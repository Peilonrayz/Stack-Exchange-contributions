import pathlib

import pytest
import matplotlib.pyplot as plt
import numpy as np

from graphtimer import Plotter, MultiTimer
import module_utils

se_code = module_utils.attr_import('se_code')

@pytest.mark.skipif(pathlib.Path('static/figs/plot-aj.png').exists(),
                    reason='Output image already exists')
def test_with_aj():
    fig, axs = plt.subplots()
    axs.set_yscale('log')
    axs.set_xscale('log')
    (
        Plotter(MultiTimer([
            se_code.peilonrayz.display,
            se_code.ajneufeld.display,
            se_code.maarten_fabre.display,
            se_code.andy.display,
        ]))
            .repeat(20, 20, np.logspace(0, 3), args_conv=lambda i: ['foo'] * int(i))
            .min()
            .plot(axs, x_label='len(flavours)')
    )
    fig.savefig('static/figs/plot-aj.png')
    fig.savefig('static/figs/plot-aj.svg')

@pytest.mark.skipif(pathlib.Path('static/figs/plot.png').exists(),
                    reason='Output image already exists')
def test_without_aj():
    fig, axs = plt.subplots()
    axs.set_yscale('log')
    axs.set_xscale('log')
    (
        Plotter(MultiTimer([
            se_code.peilonrayz.display,
            se_code.maarten_fabre.display,
            se_code.andy.display,
        ]))
            .repeat(20, 20, np.logspace(0, 5), args_conv=lambda i: ['foo'] * int(i))
            .min()
            .plot(axs, x_label='len(flavours)')
    )
    fig.savefig('static/figs/plot.png')
    fig.savefig('static/figs/plot.svg')

