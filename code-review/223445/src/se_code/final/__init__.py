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
