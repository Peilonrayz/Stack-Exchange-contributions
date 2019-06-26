import random
import copy

import numpy as np
import matplotlib.pyplot as plt
from graphtimer import Plotter, MultiTimer


def solution_justin(dungeon):
    if not dungeon or not dungeon[0]:
        return 0
    row, col = len(dungeon), len(dungeon[0])
    dp = [[0] * col for _ in range(row)]
    dp[-1][-1] = max(1, 1 - dungeon[-1][-1])

    for i in range(row - 2, -1, -1):
        dp[i][-1] = max(1, dp[i+1][-1] - dungeon[i][-1])

    for j in range(col - 2, -1, -1):
        dp[-1][j] = max(1, dp[-1][j + 1] - dungeon[-1][j])

    for i in range(row - 2, -1, -1):
        for j in range(col - 2, -1, -1):
            dp[i][j] = min(max(1, dp[i][j + 1] - dungeon[i][j]), max(1, dp[i + 1][j] - dungeon[i][j]))

    return dp[0][0]


def solution_justin_reverse(dungeon):
    if not dungeon or not dungeon[0]:
        return 0
    row, col = len(dungeon), len(dungeon[0])
    dp = [[0] * col for _ in range(row)]
    dp[-1][-1] = max(1, 1 - dungeon[-1][-1])

    for i in reversed(range(row - 1)):
        dp[i][-1] = max(1, dp[i+1][-1] - dungeon[i][-1])

    for j in reversed(range(col - 1)):
        dp[-1][j] = max(1, dp[-1][j + 1] - dungeon[-1][j])

    for i in reversed(range(row - 1)):
        for j in reversed(range(col - 1)):
            dp[i][j] = min(max(1, dp[i][j + 1] - dungeon[i][j]), max(1, dp[i + 1][j] - dungeon[i][j]))

    return dp[0][0]


def solution_justin_pre_computed(dungeon):
    if not dungeon or not dungeon[0]:
        return 0
    row, col = len(dungeon), len(dungeon[0])
    dp = [[0] * col for _ in range(row)]
    dp[-1][-1] = max(1, 1 - dungeon[-1][-1])

    rows = range(row - 2, -1, -1)
    cols = range(col - 2, -1, -1)

    for i in rows:
        dp[i][-1] = max(1, dp[i+1][-1] - dungeon[i][-1])

    for j in cols:
        dp[-1][j] = max(1, dp[-1][j + 1] - dungeon[-1][j])

    for i in rows:
        for j in cols:
            dp[i][j] = min(max(1, dp[i][j + 1] - dungeon[i][j]), max(1, dp[i + 1][j] - dungeon[i][j]))

    return dp[0][0]


def solution_justin_pre_computed_list(dungeon):
    if not dungeon or not dungeon[0]:
        return 0
    row, col = len(dungeon), len(dungeon[0])
    dp = [[0] * col for _ in range(row)]
    dp[-1][-1] = max(1, 1 - dungeon[-1][-1])

    rows = list(range(row - 2, -1, -1))
    cols = list(range(col - 2, -1, -1))

    for i in rows:
        dp[i][-1] = max(1, dp[i+1][-1] - dungeon[i][-1])

    for j in cols:
        dp[-1][j] = max(1, dp[-1][j + 1] - dungeon[-1][j])

    for i in rows:
        for j in cols:
            dp[i][j] = min(max(1, dp[i][j + 1] - dungeon[i][j]), max(1, dp[i + 1][j] - dungeon[i][j]))

    return dp[0][0]


def solution_justin_inplace(dungeon):
    if not dungeon or not dungeon[0]:
        return 0
    row, col = len(dungeon), len(dungeon[0])
    dungeon[-1][-1] = max(1, 1 - dungeon[-1][-1])

    rows = range(row - 2, -1, -1)
    cols = range(col - 2, -1, -1)

    for i in rows:
        dungeon[i][-1] = max(1, dungeon[i + 1][-1] - dungeon[i][-1])

    for j in cols:
        dungeon[-1][j] = max(1, dungeon[-1][j + 1] - dungeon[-1][j])

    for i in rows:
        for j in cols:
            dungeon[i][j] = min(
                max(1, dungeon[i][j + 1] - dungeon[i][j]),
                max(1, dungeon[i + 1][j] - dungeon[i][j])
            )

    return dungeon[0][0]


def solution_justin_no_guard(dungeon):
    dungeon[-1][-1] = max(1, 1 - dungeon[-1][-1])

    row, col = len(dungeon), len(dungeon[0])
    rows = range(row - 2, -1, -1)
    cols = range(col - 2, -1, -1)

    for i in rows:
        dungeon[i][-1] = max(1, dungeon[i + 1][-1] - dungeon[i][-1])

    for j in cols:
        dungeon[-1][j] = max(1, dungeon[-1][j + 1] - dungeon[-1][j])

    for i in rows:
        for j in cols:
            dungeon[i][j] = min(
                max(1, dungeon[i][j + 1] - dungeon[i][j]),
                max(1, dungeon[i + 1][j] - dungeon[i][j])
            )

    return dungeon[0][0]


def solution_peilonrayz(dungeon):
    dungeon[-1][-1] = min(dungeon[-1][-1], 0)
    row = len(dungeon)
    col = len(dungeon[0])
    rows = range(row - 2, -1, -1)
    cols = range(col - 2, -1, -1)

    for i in rows:
        dungeon[i][-1] = min(dungeon[i][-1] + dungeon[i + 1][-1], 0)

    for i in cols:
        dungeon[-1][i] = min(dungeon[-1][i] + dungeon[-1][i + 1], 0)

    for y in rows:
        for x in cols:
            dungeon[y][x] = max(
                min(dungeon[y][x] + dungeon[y + 1][x], 0),
                min(dungeon[y][x] + dungeon[y][x + 1], 0)
            )

    return abs(min(dungeon[0][0], 0)) + 1


memoize = {}


def create_arg(size, *, _i):
    size = int(size)
    key = size, _i
    if key in memoize:
        return copy.deepcopy(memoize[key])
    divisors = [
        (i, size // i)
        for i in range(1, int(size ** 0.5) + 1)
        if size % i == 0
    ]
    if len(divisors) > 1:
        divisors = divisors[1:]
    y_size, x_size = random.choice(divisors)
    output = [[None] * x_size for _ in range(y_size)]
    for i in range(size):
        y, x = divmod(i, x_size)
        output[y][x] = random.randint(-100, 100)
    memoize[key] = output
    return output


def main():
    fig, axs = plt.subplots()
    axs.set_yscale('log')
    axs.set_xscale('log')
    (
        Plotter(MultiTimer([
            solution_justin,
            solution_justin_reverse,
            solution_justin_pre_computed,
            solution_justin_pre_computed_list,
        ]))
            .repeat(10, 1, np.logspace(0, 2), args_conv=create_arg)
            .min()
            .plot(axs, title='Comparison of Loop Changes', x_label='dungeon size')
    )
    fig.show()

    fig, axs = plt.subplots()
    axs.set_yscale('log')
    axs.set_xscale('log')
    (
        Plotter(MultiTimer([
            solution_justin_pre_computed,
            solution_justin_inplace,
            solution_justin_no_guard,
            solution_peilonrayz,
        ]))
            .repeat(10, 1, np.logspace(0, 2), args_conv=create_arg)
            .min()
            .plot(axs, title='Code Review Changes', x_label='dungeon size')
    )
    fig.show()

    fig, axs = plt.subplots()
    axs.set_yscale('log')
    axs.set_xscale('log')
    (
        Plotter(MultiTimer([
            solution_justin,
            solution_justin_no_guard,
        ]))
            .repeat(10, 1, np.logspace(0, 2), args_conv=create_arg)
            .min()
            .plot(axs, title='Comparison of Original and Final', x_label='dungeon size')
    )
    fig.show()


if __name__ == '__main__':
    main()
