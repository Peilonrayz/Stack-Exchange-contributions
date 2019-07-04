import numpy as np

import math

CATEGORY10 = tuple('#1f77b4 #ff7f0e #2ca02c #d62728 #9467bd #8c564b #e377c2 #7f7f7f #bcbd22 #17becf'.split())
FNS = [
    lambda n: math.log(n + 1),
    lambda n: n,
    lambda n: n * math.log(n + 1),
    lambda n: n ** 2,
    lambda n: n ** 3,
    lambda n: 2 ** n,
    lambda n: math.exp(n),
    lambda n: n ** n,
]
LEGEND = [
    'log n',
    'n',
    'n log n',
    'n^2',
    'n^3',
    '2^n',
    'e^n',
    'n^n',
]
EXP = 1
DOMAINS = [np.linspace(0, 10**EXP), np.logspace(0, EXP)]


def gen_values(domain, fn):
    ret = np.array([fn(value) for value in domain])
    ret -= ret[0]
    ret /= ret[-1]
    return ret + 1


def handle_fig(fig, x, y, fns, legend):
    if x:
        fig.set_xscale('log')
    if y:
        fig.set_yscale('log')
    fig.set_title('Scale')

    domain = DOMAINS[x]
    data = [gen_values(domain, fn) for fn in fns]
    lines = [
        fig.plot(domain, ys, color=color)[0]
        for ys, color in zip(data, CATEGORY10)
    ]
    fig.legend(lines, legend, loc=0)