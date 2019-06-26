[Python command line tool for compiling py files to exec files on Mac](https://codereview.stackexchange.com/q/216510/42401) - [Shui](https://codereview.stackexchange.com/users/137924/shui)

---

I recommend that you [read PEP 8][0].

 - It's advised against doing `import os, re`. Instead have one line dedicated to each import.
 - You should have an empty line between importing third party libraries and standard library ones.
 - In Python it's standard to use `snake_case`.
 - You should only have one space either side of the equals sign when performing assignment.
 - Rather than doing `path is not ''` you should use the `!=` operator.
 - `'\.py$'` is [deprecated in Python 3.6, and will become a syntax error in a future version of Python][1]. Instead use `r'\.py$'`.
 - Don't mix `'` and `"` string delimiters. Unless it's to do `"'"`.
 - You don't need to use a `\` for line breaking as your within brackets.
 - You should have the `+` in front of the next line, rather than the end of the previous line.

---

 - Your variable names are crap. `path`, `name` `FILE`, `cFILE`, `PATH`. The reason you need your comments is because of this.
 - If you fix your variable names your comments are useless.
 - Don't make a list to then call `os.system` just call it straight away.
 - Use `pathlib`, it singlehandedly makes your code ridiculously simple.
 - Put your code in an `if __name__ == '__main__'` guard. You don't want to destroy things by accident.

<sub>untested:</sub>


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


  [0]: https://www.python.org/dev/peps/pep-0008/
  [1]: https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals