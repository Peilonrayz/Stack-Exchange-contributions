import functools

import matplotlib.pyplot as plt
import numpy as np

from graphtimer import Plotter, MultiTimer

from .changes import test_orig, test_peil, test_alain_t, test_peil_alain


@functools.lru_cache(None)
def args_conv(size):
    arr = np.arange(size)
    np.random.shuffle(arr)
    return list(arr), np.random.randint(size)


def main():
    fig, axs = plt.subplots()
    axs.set_yscale('log')
    axs.set_xscale('log')
    (
        Plotter(MultiTimer([test_orig, test_peil, test_alain_t, test_peil_alain]))
            .repeat(10, 10, np.logspace(0, 5, num=50), args_conv=args_conv)
            .min()
            .plot(axs, x_label='len(nums)')
    )
    fig.show()


if __name__ == '__main__':
    main()
