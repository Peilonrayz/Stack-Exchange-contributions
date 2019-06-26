import time
import math

import matplotlib.pyplot as plt
import numpy as np

from graphtimer import flat, Plotter, TimerNamespace


class UnoptimisedRange(object):
    def __init__(self, size):
        self.size = size

    def __getitem__(self, i):
        if i >= self.size:
            raise IndexError()
        return i


class Peilonrayz(TimerNamespace):
    def test_comprehension(iterable):
        return [i for i in iterable]

    def test_append(iterable):
        a = []
        append = a.append
        for i in iterable:
            append(i)
        return a


SCALE = 10.


class Graipher(TimerNamespace):
    def test_o_n(n):
        time.sleep(n / SCALE)

    def test_o_n2(n):
        time.sleep(n ** 2 / SCALE)

    def test_o_log(n):
        time.sleep(math.log(n + 1) / SCALE)

    def test_o_exp(n):
        time.sleep((math.exp(n) - 1) / SCALE)

    def test_o_nlog(n):
        time.sleep(n * math.log(n + 1) / SCALE)


class Reverse(TimerNamespace):
    def test_orig(stri):
        output = ''
        length = len(stri)
        while length > 0:
            output += stri[-1]
            stri, length = (stri[0:length - 1], length - 1)
        return output

    def test_g(s):
        return s[::-1]

    def test_s(s):
        return ''.join(reversed(s))


def main():
    # Reverse
    fig, axs = plt.subplots()
    axs.set_yscale('log')
    axs.set_xscale('log')
    (
        Plotter(Reverse)
            .repeat(10, 10, np.logspace(0, 5), args_conv=lambda i: ' '*int(i))
            .min()
            .plot(axs, title='Reverse', fmt='-o')
    )
    fig.show()

    # Graipher
    fig, axs = plt.subplots()
    (
        Plotter(Graipher)
            .repeat(2, 1, [i / 10 for i in range(10)])
            .min()
            .plot(axs, title='Graipher', fmt='-o')
    )
    fig.show()

    # Peilonrayz
    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
    p = Plotter(Peilonrayz)
    axis = [
        ('Range', {'args_conv': range}),
        ('List', {'args_conv': lambda i: list(range(i))}),
        ('Unoptimised', {'args_conv': UnoptimisedRange}),
    ]
    for graph, (title, kwargs) in zip(iter(flat(axs)), axis):
        (
            p.repeat(100, 5, list(range(0, 10001, 1000)), **kwargs)
                .min(errors=((-1, 3), (-1, 4)))
                .plot(graph, title=title)
        )
    fig.show()


if __name__ == '__main__':
    main()