import json
import os
import subprocess
import pathlib

__all__ = [
    'handle_post',
]

CONFIG = pathlib.Path('_configs') / 'post'


def handle_deactivate():
    paths = [
        CONFIG / 'src',
        CONFIG / 'tests',
        CONFIG / 'static',
        CONFIG / 'docs' / 'source' / 'static',
        CONFIG / 'docs' / 'source' / 'post.rst',
        CONFIG / 'docs' / 'build' / 'markdown' / 'post.md',
    ]
    for path in paths:
        if path.is_symlink():
            path.unlink()


def handle_activate(active):
    CURR = active['path']
    paths = [
        (CURR / 'src', CONFIG / 'src'),
        (CURR / 'tests', CONFIG / 'tests'),
        (CURR / 'static', CONFIG / 'static'),
        (CURR / 'static', CONFIG / 'docs' / 'source' / 'static'),
        (CURR / 'post.rst', CONFIG / 'docs' / 'source' / 'post.rst'),
        (CURR / 'post.md', CONFIG / 'docs' / 'build' / 'markdown' / 'post.md'),
    ]
    for target, link in paths:
        link.symlink_to(target, target_is_directory=target.is_dir())


def handle_active(args):
    new = False
    if args.deactivate:
        with open('.active', 'w') as f:
            f.write('{}')
        handle_deactivate()

    with open('.active') as f:
        active = json.load(f)

    if args.activate is not None:
        site, post = os.path.split(args.activate)
        new_active = {
            'site': site,
            'post': post,
            'path': args.activate
        }
        if active != new_active:
            new = True
            active = new_active

            with open('.active', 'w') as f:
                json.dump(active, f)

    if not active:
        print('No active post.')
        raise SystemExit(1)

    if args.show_active:
        print(active)
        raise SystemExit(0)

    active['path'] = pathlib.Path(active['path']).absolute()
    return new, active


def initialize_dir(path):
    folders = [
        path / 'src' / 'se_code' / 'final',
        path / 'src' / 'se_code' / 'orig',
        path / 'tests',
        path / 'static',
        path / 'static' / 'figs',
    ]
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)

    files = [
        path / 'src' / 'se_code' / '__init__.py',
        path / 'tests' / 'test_code.py',
        path / 'post.rst',
    ]
    for file in files:
        with file.open('a'):
            pass


def handle_post(args):
    new, active = handle_active(args)

    if args.initialize:
        initialize_dir(active['path'])

    if args.download:
        print('Downloading not implemented yet.')

    if args.clean:
        print('Clean not implemented yet.')

    if args.start:
        print('Start not implemented yet.')

    if new:
        handle_deactivate()
        handle_activate(active)

    if args.tox:
        subprocess.run(['tox', '-c', '_configs/post/tox.ini'])
