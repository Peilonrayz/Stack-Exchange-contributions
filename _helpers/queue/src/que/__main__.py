from . import parser, handle_post


def main():
    args = parser.parse_args()
    if getattr(args, 'queue', None) is None:
        print('Scope should be set.')
        raise SystemExit(1)

    if args.queue == 'post':
        handle_post(args)
