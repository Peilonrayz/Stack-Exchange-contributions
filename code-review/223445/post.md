Idiomatic changes & small changes:

1. Indent with 4 spaces, not 2.
1. Variable and function names should be in `lower_snake_case`.
1. Unneeded parentheses is unidiomatic.
1. Use spaces around concatenation, so `"+abc` becomes `" + abc`.
1. Use a `if __name__ == '__main__':` guard to prevent your code from running when it’s not the initialised file.
1. Have two spaces around top level function definitions.
1. “You’re” has an apostrophe in it, but you should be using “your” instead. Because you aren’t a cheapest shipping method.

Further changes:

1.  Use `if`, `elif` and `else` rather than just `if`.
1.  You can make your code dry by merging `ground_cost` and `drone_cost` together.

1. You can simplify your code by using `sorted`.

   You sort `g`, `d` and `p`. From this you can then iterate through the list and see how many are the same.

   This makes `cost_calc` contain only three simple `if` statements.

   You would have to add something like a [`enum.Enum`](https://docs.python.org/3/library/enum.html#enum.Enum) to know what type each value is, when sorting.

```
import enum


def size_cost(value, sizes):
    for size, cost in sizes[:-1]:
        if value > size:
            return cost
    return sizes[-1][1]


ground_costs = [
    (10, 4.75),
    (6, 4),
    (2, 3),
    (None, 1.5),
]
drone_cost = [
    (10, 14.25),
    (6, 12),
    (2, 9),
    (None, 4.5),
]


class Shipping(enum.Enum):
    GROUND = 'Ground'
    PREMIUM = 'Premium Ground'
    DRONE = 'Drone'


def cost_calc(weight):
    costs = [
        (Shipping.GROUND, size_cost(weight, ground_costs) * weight + 20),
        (Shipping.PREMIUM, 125),
        (Shipping.DRONE, size_cost(weight, drone_cost) * weight)
    ]
    costs.sort(key=lambda i: i[1])
    price = costs[0][1]
    costs = [s for s, p in costs if p == price]
    if len(costs) == 3:
        print("All shipping methods cost $125 according to your items weight")
    elif len(costs) == 2:
        print(
            "Your cheapest shipping method is "
            + costs[0].value
            + " shipping and "
            + costs[1].value
            + " shipping as they both cost $"
            + str(price)
        )
    else:
        print(
            "Your cheapest shipping method is "
            + costs[0].value
            + " shipping costing $"
            + str(price)
        )


if __name__ == '__main__':
    cost_calc(int(input()))
```

Output is also what you’d expect:

<!-- from se_code.final import cost_calc -->
```none
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
```

**NOTE**: [Complete changes](https://github.com/Peilonrayz/Stack-Exchange-contributions/tree/master/code-review/223445).
