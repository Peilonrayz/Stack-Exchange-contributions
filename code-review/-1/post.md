* You can use [operator.add()](https://docs.python.org/3/library/operator.html#operator.add) to remove fn.

* You’re running in $O(n^2)$ time.

```
"""Example operators library."""

from operator import add

__all__ = [
    'add',
]


def fn(a: int, b: str):
    return a+b
```

Which can be used as:

<!-- from se_code.final import add -->
```
>>> add(1, 2)
3
>>> add(1, -2)
-1
```
