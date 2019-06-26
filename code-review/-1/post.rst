* You can use :func:`operator.add` to remove `fn`.
* You're running in :math:`O(n^2)` time.

.. literalinclude:: ../../src/se_code/final/__init__.py
    :language: python

Which can be used as:

.. testsetup::

    from se_code.final import add

.. doctest::

    >>> add(1, 2)
    3
    >>> add(1, -2)
    -1
