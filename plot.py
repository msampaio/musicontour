#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pylab import grid, axis, plot, title, legend, show
import random

program_name = "Villa Lobos Contour Module v.0.1"


def random_color():
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    return colors[random.randint(0, len(colors) - 1)]


def plot_preview(cseg):
    """Generates cseg plot.

    The code is based on
    http://matplotlib.sourceforge.net/examples/pylab_examples/unicode_demo.html

    >>> plot_preview([5, 3, 4, 1, 2, 0])
    """

    grid(color='b', linestyle='-', linewidth=.1)
    axis()
    plot(cseg, linewidth=2, color=random_color(), label='{0}'.format(cseg))
    title(program_name, family='georgia', size='small')
    legend()
    show()


def multi_plot_preview(cseg_array):
    """Generates multiple cseg plot.

    [cseg, color]
    >>> multi_plot_preview([[[0, 2, 1], 'blue'], [[0, 1, 2], 'lightblue'],
                            [[0, 2, 3], 'green']])
    """

    grid(color='b', linestyle='-', linewidth=.1)
    axis()

    for cseg, color in cseg_array:
        plot(cseg, linewidth=2, color=color, label='{0}'.format(cseg))

    title(program_name, family='georgia', size='small')
    legend()
    show()
