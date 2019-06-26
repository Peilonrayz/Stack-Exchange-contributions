from typing import Any, List, Dict

import module_utils

__all__ = [
    'attrs',
]

_modules = []
module_utils.import_modules(__name__, globals(), '_modules __all__')

attrs = {}
for _module in _modules:
    for _attr in dir(_module):
        attrs.setdefault(_attr, []).append(getattr(_module, _attr))
