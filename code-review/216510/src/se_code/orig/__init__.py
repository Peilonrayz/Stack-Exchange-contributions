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
import os, re
from docopt import docopt

args = docopt(__doc__)

# the two pathnames below tell gcc where python is so that cython can be compiled to an exec
INCLUDES = '/usr/local/opt/python/Frameworks/Python.framework/Versions/3.7/include/python3.7m'
LIBRARY  = '/usr/local/Cellar/python/3.7.2_2/Frameworks/Python.framework/Versions/3.7/lib'
HIDEDATA = '&>/dev/null'  # this is used to hide output while compiling C files

for pyFILE in args['FILES']:
    if pyFILE.endswith('.py'):  # file must be a python file
        path, name = os.path.split(pyFILE)  # split full path to seperate path & filename

        cFILE  = re.sub('\.py$', '.c', pyFILE)  # name of the file with .c extension & path
        FILE   = re.sub('\.py$', '', name)  # name of the file with no extension or path

        PATH   = path + '/' if path is not '' else '.'  # if in current directory, path = '.'
        OUTPUT = args['--output'] + '/' if args['--output'] else ''  # blank if no arg given
        SHOW   = HIDEDATA if not args['--show'] else ''  # will hide gcc output if SHOW is false
        # this command will be used to delete the C file
        DELETE = f'find {PATH} -name "{FILE}.c" -type f|xargs rm -f' if args['--delete'] else ''
        RUN    = f'./{OUTPUT}{FILE}' if args['--run'] else ''  # command to run the exec

        commands = [  # cython to make C file, gcc to compile to exec, and some options
            f"cython --embed -o {cFILE} {pyFILE}",  # convert python to cython C file
            # compile cython C file to exec file
            f"gcc -v -Os -I {INCLUDES} -L {LIBRARY} {cFILE} -o {OUTPUT}{FILE} " + \
            # source python & other options -- hide or show, delete C file, run exec
            f"-lpython3.7 -lpthread -lm -lutil -ldl {SHOW}", f"{DELETE}", f"{RUN}"
        ]
        for command in commands:
            os.system(command)  # execute commands above, excluding blank commands
    else:
        print(__doc__)  # show the help menu if user doesn't put a python file