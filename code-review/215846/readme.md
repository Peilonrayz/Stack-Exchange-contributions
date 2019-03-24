[graphtimer v2 - Utility to plot timings](https://codereview.stackexchange.com/q/215846/42401) - [Peilonrayz](https://codereview.stackexchange.com/users/42401/peilonrayz)

---

[GitHub repo][1] (MIT)  
Clone the repo and replace the contents of `example.py` with the one at the bottom and you'll have everything setup.

# Explanation of the code

A long while ago I posted the question "[Abstract graphing-and-timing functions][2]".
It was a god class, wasn't extendable/configurable, you also had to use strings to interact with `timeit`.
And it just wasn't clear what was what.

A little while ago I posted an answer where I used a couple ikky `timeit.timeit` calls rather than build a graph. And Graipher showed me a nice looking graph. I've continued to see these nice graphs, with no easy way to make them myself. And so I decided I needed to way-too-early-spring clean my code.

1. (`timer.py`) A `Timer` object should be in charge of building and calling `timeit`.  
    This object was based of `timeit.Timer`, however I thought it needed some additional functionality:

    1. It should be able to time multiple functions.
    2. It should be able to test against multiple values.
    3. It should only perform timings.

2. (`graph.py`) A graph class should be introduced that plots the data in the correct way. If you want to plot in something that isn't `matplotlib` then you just need to change the class.
3. (`plotter.py`) Statistical analysis should not be in either the `Timer` or the graph class. I also kept the analysis to be pretty basic as per the [Python docs suggestion][3].
4. (`plotter.py`) Performing all the above should be simple with good defaults. And so `Plotter` handles interacting with everything. Whilst it's a small wrapper it means that I, and other, don't have to write that many lines to get the wanted graph.

# What I'd like out of a review.

1. The thing I find most important right now is, [is the design good][4]?

    Is `Plotter` a poor design pattern? Is splitting the code out like I have done a bad idea?

2. Is the usage for a user clean and readable?
3. Is there a way to make my code more readable? I find `MatPlotLib` to be a bit on the not so clean side.
4. Any and all critiques are welcome.

# Code

(I have left out some code, and the .pyi files. These are available [on GitHub][1].)

`graph.py`

    from .graphtimer import CATEGORY10


    class MatPlotLib:
        def _graph_times(self, graph, data, domain, colors, error, fmt):
            for results, color in zip(data, colors):
                values = [v.value for v in results]
                if error:
                    errors = zip(*[v.errors or [] for v in results])
                    for error in errors:
                        lower, upper = zip(*error)
                        graph.fill_between(domain, upper, lower, facecolor=color, edgecolor=None, alpha=0.1)
                yield graph.plot(domain, values, fmt, color=color)[0]

        def graph(self, graph, data, domain, *, functions=None, colors=CATEGORY10, title=None, legend=True, error=True,
                  x_label='Input', y_label='Time [s]', fmt='-'):
            lines = list(self._graph_times(graph, data, domain, colors, error, fmt))
            if x_label is not None:
                graph.set_xlabel(x_label)
            if y_label is not None:
                graph.set_ylabel(y_label)
            if title is not None and hasattr(graph, 'set_title'):
                graph.set_title(title)
            if legend and functions is not None and hasattr(graph, 'legend'):
                graph.legend(lines, [fn.__name__ for fn in functions], loc=0)
            return lines

`timers.py`

    import timeit

    SENTINAL = object()


    class MultiTimer:
        """Interface to timeit.Timer to ease timing over multiple functions."""
        def __init__(self, functions, timer=timeit.Timer):
            self.timer = timer
            self.functions = functions

        def build_timer(self, fn, domain, stmt='fn(*args)', setup='pass', timer=SENTINAL, globals=SENTINAL,
                        args_conv=SENTINAL):
            """Build a timeit.Timer"""
            if not isinstance(domain, tuple):
                domain = domain,
            if args_conv is not SENTINAL:
                domain = args_conv(*domain)
                if not isinstance(domain, tuple):
                    domain = domain,

            if globals is SENTINAL:
                globals = {}
            else:
                globals = globals.copy()
            globals.update({'fn': fn, 'args': domain})

            # print(f'{self.timer}({stmt!r}, {setup!r}, {timer!r}, {globals!r})')

            if timer is SENTINAL:
                timer = timeit.default_timer

            return self.timer(stmt, setup, timer, globals=globals)

        def build_timers(self, domain, *args, **kwargs):
            """Build multiple timers from various inputs and functions"""
            return [
                [
                    self.build_timer(fn, dom, *args, **kwargs)
                    for fn in self.functions
                ]
                for dom in domain
            ]

        def _call(self, domain, repeat, call, *args, **kwargs):
            """Helper function to generate timing data."""
            if len(domain) == 0:
                raise ValueError('domain must have at least one argument.')

            functions = self.build_timers(domain, *args, **kwargs)
            output = [[[] for _ in domain] for _ in functions[0]]
            for _ in range(repeat):
                for j, fns in enumerate(functions):
                    for i, fn in enumerate(fns):
                        output[i][j].append(call(fn))
            return output

        def repeat(self, domain, repeat, number, *args, **kwargs):
            """Interface to timeit.Timer.repeat. `domain` is the values to pass to the functions."""
            return self._call(domain, repeat, lambda f: f.timeit(number), *args, **kwargs)

        def timeit(self, domain, number, *args, **kwargs):
            """Interface to timeit.Timer.timeit. `domain` is the values to pass to the functions."""
            return [
                [value[0] for value in values]
                for values in self.repeat(domain, 1, number, *args, **kwargs)
            ]

        def autorange(self, domain, *args, **kwargs):
            """Interface to timeit.Timer.autorange. `domain` is the values to pass to the functions."""
            return [
                [value[0] for value in values]
                for values in self._call(domain, 1, lambda f: f.autorange(), *args, **kwargs)
            ]


    class TimerNamespaceMeta(type):
        """Convenience class to ease creation of a MultiTimer."""
        def __new__(mcs, name, bases, attrs):
            if 'functions' in attrs:
                raise TypeError('FunctionTimers cannot define `functions`')
            if 'multi_timer' in attrs:
                raise TypeError('FunctionTimers cannot define `multi_timer`')

            ret: TimerNamespace = super().__new__(mcs, name, bases, attrs)
            functions = [v for k, v in attrs.items() if k.startswith('test')]
            ret.functions = functions
            ret.multi_timer = ret.MULTI_TIMER(functions, ret.TIMER)
            return ret


    class TimerNamespace(metaclass=TimerNamespaceMeta):
        """Convenience class to ease creation of a MultiTimer."""
        TIMER = timeit.Timer
        MULTI_TIMER = MultiTimer

`plotter.py`

    from .graph import MatPlotLib


    class Plotter:
        """Interface to the timer object. Returns objects made to ease usage."""
        def __init__(self, timer):
            self.timer = getattr(timer, 'multi_timer', timer)

        def timeit(self, number, domain, *args, **kwargs):
            """Interface to self.timer.timeit. Returns a PlotValues."""
            return self.repeat(1, number, domain, *args, **kwargs).min(errors=None)

        def repeat(self, repeat, number, domain, *args, **kwargs):
            """Interface to self.timer.repeat. Returns a PlotTimings."""
            return PlotTimings(
                self.timer.repeat(domain, repeat, number, *args, **kwargs),
                {
                    'functions': self.timer.functions,
                    'domain': domain
                }
            )


    class _DataSet:
        """Holds timeit values and defines statistical methods around them."""
        def __init__(self, values):
            self.values = sorted(values)

        def quartile_indexes(self, outlier):
            """Generates the quartile indexes. Uses tukey's fences to remove outliers."""
            delta = (len(self.values) - 1) / 4
            quartiles = [int(round(delta * i)) for i in range(5)]
            if outlier is not None:
                if outlier < 0:
                    raise ValueError("outlier should be non-negative.")
                iqr = outlier * (self.values[quartiles[3]] - self.values[quartiles[1]])
                low = self.values[quartiles[1]] - iqr
                high = self.values[quartiles[3]] + iqr

                for i, v in enumerate(self.values):
                    if v >= low:
                        quartiles[0] = i
                        break

                for i, v in reversed(list(enumerate(self.values))):
                    if v <= high:
                        quartiles[4] = i
                        break
            return tuple(quartiles)

        def errors(self, errors, outlier):
            """Returns tuples containing the quartiles wanted."""
            if errors is None:
                return None
            quartiles = self.quartile_indexes(outlier)
            # Allow out of quartile error bars using -1 and 5.
            quartiles += (-1, 0)
            return [
                (
                    self.values[quartiles[start]],
                    self.values[quartiles[stop]]
                )
                for start, stop in errors
            ]

        def quartile(self, quartile, outlier):
            """Return the value of the quartile provided."""
            quartiles = self.quartile_indexes(outlier)
            return self.values[quartiles[quartile]]

        def mean(self, start, end, outlier):
            """Return the mean of the values over the quartiles specified."""
            quartiles = self.quartile_indexes(outlier)
            start = quartiles[start]
            end = quartiles[end]
            return sum(self.values[start:end + 1]) / (1 + end - start)


    class PlotTimings:
        """Thin interface over _DataSet"""
        def __init__(self, data, kwargs):
            self.data = [
                [_DataSet(results) for results in function_values]
                for function_values in data
            ]
            self.kwargs = kwargs

        def quartile(self, quartile, *, errors=None, outlier=1.5):
            """Interface to _DataSet.quartile and errors. Returns a PlotValues."""
            return PlotValues(
                [
                    [
                        _DataValues(
                            ds.quartile(quartile, outlier),
                            ds.errors(errors, outlier)
                        )
                        for ds in function_values
                    ]
                    for function_values in self.data
                ],
                self.kwargs
            )

        def min(self, *, errors=((-1, 3),), outlier=1.5):
            """Return the Q1 value and show the error from Q-1 Q3."""
            return self.quartile(0, errors=errors, outlier=outlier)

        def max(self, *, errors=((1, 5),), outlier=1.5):
            """Return the Q4 value and show the error from Q1 Q5."""
            return self.quartile(4, errors=errors, outlier=outlier)

        def mean(self, start=0, end=4, *, errors=((1, 3),), outlier=1.5):
            """Interface to _DataSet.mean and errors. Returns a PlotValues."""
            return PlotValues(
                [
                    [
                        _DataValues(
                            ds.mean(start, end, outlier),
                            ds.errors(errors, outlier)
                        )
                        for ds in function_values
                    ]
                    for function_values in self.data
                ],
                self.kwargs
            )


    class _DataValues:
        """Holds the wanted statistical data from the timings."""
        def __init__(self, value, errors):
            self.value = value
            self.errors = errors


    class PlotValues:
        """Thin interface to Graph.graph."""
        def __init__(self, data, kwargs):
            self.data = data
            self.kwargs = kwargs

        def plot(self, graph, graph_lib=MatPlotLib, **kwargs):
            g = graph_lib()
            return g.graph(
                graph,
                self.data,
                self.kwargs.pop('domain'),
                functions=self.kwargs.pop('functions'),
                **kwargs
            )


# Example usage

I've included the same graph as I did on my old code. And two of Graipher's graphs.

1. [Abstract graphing-and-timing functions][2] - This is to ensure usage is simple in abnormal usage.  
    It also shows that you can plot multiple error areas, highlighted in the unoptimised graph.

2. [Plot timings for a range of inputs][5] - This is to make sure standard usage is simple.
3. [String reversal in Python][6] - This is so I know logerithmic graphs display correctly.

    I'm running on Windows and don't have a C compiler, and so I can't include the additional two functions. However I think it nicely shows why the Python docs say to use `min`.

<!---->

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

[![My graphs][7]][7]
[![Graipher's graphs][8]][8]
[![Reverse graphs][9]][9]


  [1]: https://github.com/Peilonrayz/graphtimer
  [2]: https://codereview.stackexchange.com/q/146434
  [3]: https://docs.python.org/3.7/library/timeit.html#timeit.Timer.repeat
  [4]: https://codereview.meta.stackexchange.com/a/1926
  [5]: https://codereview.stackexchange.com/q/165245
  [6]: https://codereview.stackexchange.com/a/215181
  [7]: https://i.stack.imgur.com/Nx6Ia.png
  [8]: https://i.stack.imgur.com/Csvbr.png
  [9]: https://i.stack.imgur.com/RHIhE.png