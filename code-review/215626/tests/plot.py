import matplotlib.pyplot as plt

from graphtimer import Plotter, MultiTimer

from se_code.changes import available, test_orig, test_early_leaf, test_peil


def main():
    def args_conv(size):
        return available, size

    fig, axs = plt.subplots()
    axs.set_yscale('log')
    # axs.set_xscale('log')
    (
        Plotter(MultiTimer([test_orig, test_early_leaf, test_peil]))
            .repeat(5, 5, range(100, 201, 10), args_conv=args_conv)
            .min()
            .plot(axs, x_label='len(nums)')
    )
    fig.show()


if __name__ == '__main__':
    main()
