"""(PYCX) PYthon to Cython to eXec, a unix command line util
Usage:
  pycx FILES... [-o DIR --show --delete --run]
  pycx --help

Options:
  FILES              one or more python files to compile
  -o --output=DIR    output directory
  -s --show          show output from exec compiling
  -d --delete        delete the c file after compiling exec
  -r --run           run the exec after compiling
  -h --help          show this screen.
"""
import os
from pathlib import Path

from docopt import docopt


INCLUDES = '/usr/local/opt/python/Frameworks/Python.framework/Versions/3.7/include/python3.7m'
LIBRARY = '/usr/local/Cellar/python/3.7.2_2/Frameworks/Python.framework/Versions/3.7/lib'
HIDEDATA = '&>/dev/null'


def main(args):
    for path in args['FILES']:
        path = Path(path)
        if path.suffix != '.py':
            print(__doc__)
            continue

        output = Path(args['--output'] or '') / path.stem
        c_file = path.parent / path.stem + '.c'

        os.system(f'cython --embed -o {c_file} {path}')
        os.system(
            f'gcc -v -Os -I {INCLUDES} -L {LIBRARY} {c_file} '
            f'-o {output} -lpython3.7 -lpthread -lm -lutil -ldl '
            + HIDEDATA if not args['--show'] else ''
        )

        if args['--delete']:
            os.system(
                f'find {path.parent} -name "{path.stem}.c" -type f'
                f'|xargs rm -f'
            )

        if args['--run']:
            os.system(f'{output}')


if __name__ == '__main__':
    main(docopt(__doc__))
