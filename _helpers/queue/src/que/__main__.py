from . import parser, handle_post


def main():
    args = parser.parse_args()
    if getattr(args, 'queue', None) is None:
        print('Scope should be set.')
        raise SystemExit(1)

    if args.queue == 'new':
        args.queue = 'post'
        args.initialize = True
        args.download = True
        args.clean = True
        args.start = True
        args.tox = True

        args.deactivate = False
        args.show_active = False

    if args.queue == 'post':
        handle_post(args)
