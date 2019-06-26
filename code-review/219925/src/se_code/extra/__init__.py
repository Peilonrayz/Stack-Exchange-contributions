import math

import matplotlib.pyplot as plt
import numpy as np

from graphtimer import Plotter, MultiTimer

LIMIT = 10000


def random_none(amount):
    return [
        np.random.randint(LIMIT)
        for _ in range(amount)
    ]


def random_chunked_10(amount):
    return [
        value
        for _ in range(int(math.ceil(amount / 10)))
        for value in np.random.randint(LIMIT, size=10)
    ]


def random_chunked_50(amount):
    return [
        value
        for _ in range(int(math.ceil(amount / 50)))
        for value in np.random.randint(LIMIT, size=50)
    ]


def random_chunked_100(amount):
    return [
        value
        for _ in range(int(math.ceil(amount / 100)))
        for value in np.random.randint(LIMIT, size=100)
    ]


def random_chunked_500(amount):
    return [
        value
        for _ in range(int(math.ceil(amount / 500)))
        for value in np.random.randint(LIMIT, size=500)
    ]


def main():
    fig, axs = plt.subplots()
    axs.set_yscale('log')
    axs.set_xscale('log')
    (
        Plotter(MultiTimer([
            random_none,
            random_chunked_10,
            random_chunked_50,
            random_chunked_100,
            random_chunked_500,
        ]))
            .repeat(5, 5, np.logspace(0, 5), args_conv=lambda n: int(n))
            .min()
            .plot(axs, title='Randoms')
    )
    fig.show()


if __name__ == '__main__':
    main()
