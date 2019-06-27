import importlib
import pkgutil
import os.path
import contextlib
import itertools
import typing


def _walk_modules(module_info, *, import_package=False, import_module=False, recursive=False):
    get_modules = (pkgutil.walk_packages if recursive else pkgutil.iter_modules)
    paths = [module_info.module_finder.path]
    prefix = '' if module_info.name == '__main__' else module_info.name + '.'
    for module_info in get_modules(paths, prefix):
        if import_package if module_info.ispkg else import_module:
            module = importlib.import_module(module_info.name)
        else:
            module = None
        yield module_info, module


def walk_modules(module_info, *, import_package=False, import_module=False, recursive=False):
    if recursive and not import_package:
        raise ValueError('recursive must import packages.')
    return list(_walk_modules(
        module_info,
        import_package=import_package,
        import_module=import_module,
        recursive=recursive,
    ))


class _GlobalsModule(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError() from e

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        del self[key]


class _TreeNode:
    def __init__(self):
        self.module = None
        self._children = {}

    def _get(self, path):
        node = self
        for key in path.split('.'):
            node = node._children.setdefault(key, _TreeNode())
            yield node

    def __getitem__(self, path):
        return [n.module for n in self._get(path)]

    def __setitem__(self, path, value):
        list(self._get(path))[~0].module = value

    def __iter__(self):
        return iter((key, n.module) for key, n in self._children.items())

    def walk(self, key=None):
        yield key, self.module
        if key is None:
            for k, node in self._children.items():
                yield from node.walk(k)
        else:
            for k, node in self._children.items():
                yield from node.walk(key + '.' + k)


def add_qualname(modules):
    for module_info, module in modules:
        module.__qualname__ = '.'.join(module_info.name)
        for attr in dir(module):
            item = getattr(module, attr)
            if hasattr(item, '__name__'):
                try:
                    item.__qualname__ = '.'.join([module_info.name, item.__name__])
                except AttributeError:
                    pass


def build_tree(modules):
    root = _TreeNode()
    for module_info, module in modules:
        root[module_info.name] = module
    return root


def append_attr(tree, attr):
    SENTINEL = object()
    for key, module in tree.walk():
        if module is None or '.' not in key:
            continue
        parent = tree[key][~1]
        item = getattr(parent, attr, SENTINEL)
        if item is SENTINEL:
            item = []
            setattr(parent, attr, item)
        item.append(module)


def _build_module_info(name):
    loader = pkgutil.get_loader(name)
    path = os.path.dirname(loader.path)
    return pkgutil.ModuleInfo(
        pkgutil.get_importer(path),
        name,
        loader.is_package(name),
    )


@contextlib.contextmanager
def load_unimportable(name, globals):
    self = _GlobalsModule(globals or {})
    try:
        yield (
            _build_module_info(name),
            self,
        )
    finally:
        for key, value in self.items():
            globals[key] = value


@contextlib.contextmanager
def load_importable(name):
    try:
        self = importlib.import_module(name)
        yield (
            _build_module_info(name),
            self,
        )
    finally:
        pass


def import_modules(name, globals=None, attrs='__all__'):
    with load_unimportable(name, globals) as (module_info, module):
        modules = walk_modules(module_info, recursive=True, import_package=True, import_module=True)
        add_qualname(modules)
        tree = build_tree(modules)
        tree[name] = module
        for attr in attrs.split():
            append_attr(tree, attr)


SENTINEL = object()


class Recursive(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = None

    def __missing__(self, key):
        value = Recursive()
        self[key] = value
        return value


def group_modules(modules, name):
    name_len = len(name.split('.'))
    tree = Recursive()
    for info, child in modules:
        if not info.name.startswith(name):
            continue

        node = tree
        for seg in info.name.split('.')[name_len:]:
            node = node[seg]
        node.value = child
    return tree


class TransparentModule:
    def __init__(self, tree):
        self.module = tree.value
        self.modules = {
            key: type(self)(value)
            for key, value in tree.items()
        }

    def __repr__(self):
        return f'TransparentModule({self.module})'

    def __getattr__(self, item):
        try:
            value = self.modules[item]
        except KeyError:
            value = getattr(self.module, item)
        setattr(self, item, value)
        return value

    @classmethod
    def build(cls, module_info, module=None):
        if module is None:
            module = importlib.import_module(module_info.name)

        children = walk_modules(module_info, recursive=True, import_package=True, import_module=True)
        add_qualname(children)
        group = group_modules(children, module_info.name)
        group.value = module
        return cls(group)


class TransparentAttrsModule(TransparentModule):
    __attrs = None

    def attrs(self):
        attrs = {}
        for module in self.modules.values():
            for _attr in dir(module.module):
                attrs.setdefault(_attr, []).append(getattr(module, _attr))
        return attrs


def transparent_import(name, cls=TransparentModule):
    with load_importable(name) as (module_info, module):
        return cls.build(module_info, module)


def attr_import(name):
    return transparent_import(name, TransparentAttrsModule)
