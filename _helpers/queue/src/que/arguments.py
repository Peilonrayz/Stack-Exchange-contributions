import argparse

__all__ = [
    'parser',
]

parser = argparse.ArgumentParser(description='Ease Stack Exchange posts')
subparsers = parser.add_subparsers()
post = subparsers.add_parser('post',
                             help='Perform actions on a specific post.')
post.set_defaults(queue='post')
deactive = post.add_mutually_exclusive_group()
deactive.add_argument('-a', '--activate', type=str, help='activate post id')
deactive.add_argument('-d', '--deactivate', action='store_true',
                      help='deactivate post id')
deactive.add_argument('-A', '--show_active', action='store_true',
                      help='show active post')
post.add_argument('-i', '--initialize', action='store_true',
                  help='initialize folder')
post.add_argument('-D', '--download', action='store_true',
                  help='download post')
post.add_argument('-c', '--clean', action='store_true', help='clean post')
post.add_argument('-s', '--start', action='store_true', help='start post')
post.add_argument('-t', '--tox', action='store_true', help='tox post')

se = subparsers.add_parser('se')
se.set_defaults(queue='se')

se = subparsers.add_parser('new')
se.set_defaults(queue='new')
se.add_argument('activate', type=str, help='activate post id')
