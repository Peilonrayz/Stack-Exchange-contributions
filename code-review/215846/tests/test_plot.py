import pathlib

import pytest
import matplotlib.pyplot as plt
import numpy as np

from graphtimer import flat, Plotter, MultiTimer

import se_code

from plot_helpers import FNS, LEGEND, handle_fig


@pytest.mark.skipif(pathlib.Path('static/figs/reverse.png').exists(),
                    reason='Output image already exists')
def test_reverse_plot():
    fig, axs = plt.subplots()
    axs.set_yscale('log')
    axs.set_xscale('log')
    (
        Plotter(se_code.Reverse)
            .repeat(10, 10, np.logspace(0, 5), args_conv=lambda i: ' '*int(i))
            .min()
            .plot(axs, title='Reverse', fmt='-o')
    )
    fig.savefig('static/figs/reverse.png')
    fig.savefig('static/figs/reverse.svg')


@pytest.mark.skipif(pathlib.Path('static/figs/graipher.png').exists(),
                    reason='Output image already exists')
def test_graipher_plot():
    fig, axs = plt.subplots()
    (
        Plotter(se_code.Graipher)
            .repeat(2, 1, [i / 10 for i in range(10)])
            .min()
            .plot(axs, title='Graipher', fmt='-o')
    )
    fig.savefig('static/figs/graipher.png')
    fig.savefig('static/figs/graipher.svg')


@pytest.mark.skipif(pathlib.Path('static/figs/peilonrayz.png').exists(),
                    reason='Output image already exists')
def test_peilonrayz_plot():
    fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)
    p = Plotter(se_code.Peilonrayz)
    axis = [
        ('Range', {'args_conv': range}),
        ('List', {'args_conv': lambda i: list(range(i))}),
        ('Unoptimised', {'args_conv': se_code.UnoptimisedRange}),
    ]
    for graph, (title, kwargs) in zip(iter(flat(axs)), axis):
        (
            p.repeat(100, 5, list(range(0, 10001, 1000)), **kwargs)
                .min(errors=((-1, 3), (-1, 4)))
                .plot(graph, title=title)
        )
    fig.savefig('static/figs/peilonrayz.png')
    fig.savefig('static/figs/peilonrayz.svg')


@pytest.mark.skipif(pathlib.Path('static/figs/scale_ex_ex.png').exists(),
                    reason='Output image already exists')
def test_scale_ex_ex_plot():
    fig, axs = plt.subplots()
    handle_fig(axs, 1, 1, FNS, LEGEND)
    fig.savefig('static/figs/scale_ex_ex.png')
    fig.savefig('static/figs/scale_ex_ex.svg')


@pytest.mark.skipif(pathlib.Path('static/figs/scale_ex_ln.png').exists(),
                    reason='Output image already exists')
def test_scale_ex_ln_plot():
    fig, axs = plt.subplots()
    handle_fig(axs, 1, 0, FNS, LEGEND)
    fig.savefig('static/figs/scale_ex_ln.png')
    fig.savefig('static/figs/scale_ex_ln.svg')


@pytest.mark.skipif(pathlib.Path('static/figs/scale_ln_ex.png').exists(),
                    reason='Output image already exists')
def test_scale_ln_ex_plot():
    fig, axs = plt.subplots()
    handle_fig(axs, 0, 1, FNS, LEGEND)
    fig.savefig('static/figs/scale_ln_ex.png')
    fig.savefig('static/figs/scale_ln_ex.svg')


@pytest.mark.skipif(pathlib.Path('static/figs/scale_ln_ln.png').exists(),
                    reason='Output image already exists')
def test_scale_ln_ln_plot():
    fig, axs = plt.subplots()
    handle_fig(axs, 0, 0, FNS, LEGEND)
    fig.savefig('static/figs/scale_ln_ln.png')
    fig.savefig('static/figs/scale_ln_ln.svg')
