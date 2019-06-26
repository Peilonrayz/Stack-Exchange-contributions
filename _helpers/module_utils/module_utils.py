import importlib
import pkgutil
import os.path
import contextlib


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
