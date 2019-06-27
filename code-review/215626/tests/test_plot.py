import pathlib

import pytest
import matplotlib.pyplot as plt

from graphtimer import Plotter, MultiTimer
import module_utils

se_code = module_utils.attr_import('se_code')
attrs = se_code.attrs()

@pytest.mark.skipif(pathlib.Path('static/figs/all_plots.png').exists(),
                    reason='Output image already exists')
def test_all_plots():
    def args_conv(size):
        return se_code.final.available, size

    fig, axs = plt.subplots()
    axs.set_yscale('log')
    # axs.set_xscale('log')
    (
        Plotter(MultiTimer([
            se_code.cleaned.find_combs,
            se_code.early_leaf.find_combs,
            se_code.early_leaf_memo.find_combs,
            se_code.final.find_combs,
        ]))
            .repeat(5, 5, range(100, 201, 10), args_conv=args_conv)
            .min()
            .plot(axs, x_label='len(nums)')
    )
    fig.savefig('static/figs/all_plots.png')
    fig.savefig('static/figs/all_plots.svg')


@pytest.mark.skipif(pathlib.Path('static/figs/final.png').exists(),
                    reason='Output image already exists')
def test_all_plots():
    def args_conv(size):
        return se_code.final.available, size

    fig, axs = plt.subplots()
    # axs.set_yscale('log')
    # axs.set_xscale('log')
    (
        Plotter(MultiTimer([
            se_code.final.find_combs,
        ]))
            .repeat(5, 5, range(0, 2001, 10), args_conv=args_conv)
            .min()
            .plot(axs, x_label='len(nums)')
    )
    fig.savefig('static/figs/final.png')
    fig.savefig('static/figs/final.svg')
