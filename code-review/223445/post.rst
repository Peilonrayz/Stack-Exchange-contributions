Idiomatic changes & small changes:

1. Indent with 4 spaces, not 2.
1. Variable and function names should be in :code:`lower_snake_case`.
1. Unneeded parentheses is unidiomatic.
1. Use spaces around concatenation, so :code:`"+abc` becomes :code:`" + abc`.
1. Use a :code:`if __name__ == '__main__':` guard to prevent your code from running when it's not the initialised file.
1. Have two spaces around top level function definitions.
1. "You're" has an apostrophe in it, but you should be using "your" instead. Because you aren't a cheapest shipping method.

Further changes:


1.  Use :code:`if`, :code:`elif` and :code:`else` rather than just :code:`if`.
1.  You can make your code dry by merging :code:`ground_cost` and :code:`drone_cost` together.

1.  You can simplify your code by using :code:`sorted`.

    You sort :code:`g`, :code:`d` and :code:`p`. From this you can then iterate through the list and see how many are the same.

    This makes :code:`cost_calc` contain only three simple :code:`if` statements.

    You would have to add something like a :class:`enum.Enum` to know what type each value is, when sorting.

.. literalinclude:: ../../src/se_code/final/__init__.py
    :language: python

Output is also what you'd expect:

.. testsetup::

    from se_code.final import cost_calc

.. doctest::

    >>> cost_calc(1)
    Your cheapest shipping method is Drone shipping costing $4.5
    >>> cost_calc(5)
    Your cheapest shipping method is Ground shipping costing $35
    >>> cost_calc(1000)
    Your cheapest shipping method is Premium Ground shipping costing $125
    >>> cost_calc(10 / 3)
    Your cheapest shipping method is Ground shipping and Drone shipping as they both cost $30.0
    >>> cost_calc(105 / 4.75)
    Your cheapest shipping method is Ground shipping and Premium Ground shipping as they both cost $125.0

.. note::

    `Complete changes <https://github.com/Peilonrayz/Stack-Exchange-contributions/tree/master/code-review/223445>`_.
