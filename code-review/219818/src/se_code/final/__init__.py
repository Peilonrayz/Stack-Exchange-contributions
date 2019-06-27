import collections
import itertools
import operator
import functools

import matplotlib.pyplot as plt
import numpy as np

from graphtimer import Plotter, MultiTimer


def largest_orig(values):
    max_no = 0
    for i in values:
        if i > max_no:
            max_no = i
            high = [i]
        elif i == max_no:
            high.append(i)
    return high


def largest_orig_pretty(values):
    max_no = 0
    highest = []
    for value in values:
        if value > max_no:
            max_no = value
            highest = [value]
        elif value == max_no:
            highest.append(value)
    return highest


def largest_no_max(values):
    if not values:
        return []
    highest = [values[0]]
    for value in values[1:]:
        if value > highest[0]:
            highest = [value]
        elif value == highest[0]:
            highest.append(value)
    return highest


def largest_no_max_iter(values):
    values = iter(values)
    highest = [next(values)]
    for value in values:
        if value > highest[0]:
            highest = [value]
        elif value == highest[0]:
            highest.append(value)
    return highest


def largest_counter(values):
    if not values:
        return []
    c = collections.Counter(values)
    k = max(c)
    return [k] * c[k]


def largest_sort(values):
    if not values:
        return []
    values.sort(reverse=True)
    value = values[0]
    for i, v in enumerate(values):
        if value != v:
            return [value] * i
    return values


def largest_sort_semifunctional(values):
    if not values:
        return []
    values.sort(reverse=True)
    value = values[0]
    return list(itertools.takewhile(lambda i: i == value, values))


def largest_sort_functional(values):
    if not values:
        return []
    values.sort(reverse=True)
    value = values[0]
    return list(itertools.takewhile(functools.partial(operator.eq, value), values))


def largest_sorted(values):
    if not values:
        return []
    values = sorted(values, reverse=True)
    value = values[0]
    for i, v in enumerate(values):
        if value != v:
            return [value] * i
    return values


# Independently created
# Same as https://stackoverflow.com/a/55216417
# By Allan - https://stackoverflow.com/users/8794221/allan
def largest_max_count(values):
    if not values:
        return []
    maximum = max(values)
    return [maximum] * values.count(maximum)


# Derived from https://stackoverflow.com/a/55216309
# By Ev. Kounis - https://stackoverflow.com/users/6162307/ev-kounis
def largest_max_count_comprehension(values):
    if not values:
        return []
    maximum = max(values)
    return [maximum for _ in range(values.count(maximum))]


# Derived from https://stackoverflow.com/a/55216401
# By Daweo - https://stackoverflow.com/users/10785975/daweo
def largest_max_comprehension(values):
    if not values:
        return []
    return [value for value in values if value == max(values)]


# Derived from https://stackoverflow.com/a/55216401
# By Daweo - https://stackoverflow.com/users/10785975/daweo
def largest_max_comprehension_once(values):
    if not values:
        return []
    maximum = max(values)
    return [value for value in values if value == maximum]


# Derived from https://stackoverflow.com/a/55254044
# By Grijesh Chauhan - https://stackoverflow.com/a/55254044
def largest_grijesh_chauhan(iterable):
    max = None
    count = 0
    for index, value in enumerate(iterable):
        if index == 0 or value >= max:
            if value != max:
                count = 0
            max = value
            count += 1
    return count * [max]


def main():
    fig, axs = plt.subplots()
    axs.set_yscale('log')
    axs.set_xscale('log')
    (
        Plotter(MultiTimer([
            largest_orig,
            largest_orig_pretty,
            largest_no_max,
            largest_no_max_iter,
            largest_counter,
            largest_sort,
            largest_sort_semifunctional,
            largest_sort_functional,
            largest_sorted,
            largest_max_count,
        ]))
            .repeat(10, 10, np.logspace(0, 5), args_conv=lambda n: list(np.random.rand(int(n))))
            .min()
            .plot(axs, title='Maximums')
    )
    fig.show()

    fig, axs = plt.subplots()
    axs.set_yscale('log')
    axs.set_xscale('log')
    (
        Plotter(MultiTimer([
            largest_orig_pretty,
            largest_sort,
            largest_max_count,
            largest_max_count_comprehension,
            largest_max_comprehension,
            largest_max_comprehension_once,
            largest_grijesh_chauhan,
        ]))
            .repeat(10, 10, np.logspace(0, 3), args_conv=lambda n: list(np.random.rand(int(n))))
            .min()
            .plot(axs, title='Maximums SO comparison')
    )
    fig.show()


if __name__ == '__main__':
    main()
