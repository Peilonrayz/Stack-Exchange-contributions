import random
import copy

import numpy as np
import matplotlib.pyplot as plt
from graphtimer import Plotter, MultiTimer


# Derived from https://codereview.stackexchange.com/q/221858/42401
# By Justin - https://codereview.stackexchange.com/users/195671/justin
def solution_justin(n):
    a = []

    for i in range(n):
        a.append([])
        a[i].append(1)

        for j in range(1, i):
            a[i].append(a[i - 1][j - 1] + a[i - 1][j])
        if i != 0:
            a[i].append(1)
    return a


# Derive from https://codereview.stackexchange.com/a/221873/42401
# By AJNeufeld - https://codereview.stackexchange.com/users/100620/ajneufeld
def solution_ajneufeld(n):
    output = [[1]]
    row = [1]
    for _ in range(n - 1):
        row = [1] + [x + y for x, y in zip(row[:-1], row[1:])] + [1]
        output.append(row)
    return output


# Derived from https://codereview.stackexchange.com/a/221862/42401
# By Josay - https://codereview.stackexchange.com/users/9452/josay
def solution_josay(n):
    p = []
    for i in range(n):
        line = [1]
        if i:
            prev_line = p[-1]
            for j in range(1, i):
                line.append(prev_line[j - 1] + prev_line[j])
            line.append(1)
        p.append(line)
    return p


# Derived from https://codereview.stackexchange.com/a/221924/42401
# By Rishav - https://codereview.stackexchange.com/users/77159/rishav
def solution_rishav(n):
    output = []
    for i in range(n):
        numerator, denominator = i, 1
        cur = 1
        row = []
        for _ in range(i + 1):
            row.append(cur)
            cur = (cur * numerator) // denominator
            numerator -= 1
            denominator += 1
        output.append(row)
    return output


def solution_rishav_np(n):
    nums = np.arange(1, n)
    output = [[1]]
    for i in range(1, n):
        output.append([1] + list(np.cumprod(nums[i-1::-1]) // nums[:i]))
    return output


def main():
    if True:
        fig, axs = plt.subplots()
        axs.set_yscale('log')
        axs.set_xscale('log')
        (
            Plotter(MultiTimer([
                solution_justin,
                solution_ajneufeld,
                solution_josay,
                solution_rishav,
                solution_rishav_np,
            ]))
                .repeat(10, 1, np.logspace(0, 2), args_conv=int)
                .min()
                .plot(axs, title='Comparison of Answers', x_label='n')
        )
        fig.show()

    if True:
        output = None
        amount = 1000
        for fn in [
            solution_justin,
            solution_ajneufeld,
            solution_josay,
            solution_rishav,
            solution_rishav_np,
        ]:
            if output is None:
                output = fn(amount)
            elif output != fn(amount):
                print(fn)
                #print(output)
                #print(fn(amount))


if __name__ == '__main__':
    main()
