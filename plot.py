#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pylab import grid, axis, plot, title, legend, show, xticks, yticks, \
     figure, ylabel, xlabel
from matplotlib.font_manager import FontProperties

from contour import Contour
from utils import flatten
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

    cseg_yticks = range((min(cseg)), (max(cseg) + 1))
    cseg_xticks = range(len(cseg))

    ## These commands don't allow the plotting the same window in GUI
    # fig = figure()
    # fig.canvas.set_window_title(program_name)

    grid(color='b', linestyle='-', linewidth=.1)
    axis()

    title_name = program_name + " --- Contour plotter"
    xlabel('c-pitch position')
    ylabel('c-pitch')
    xticks(cseg_xticks)
    yticks(cseg_yticks)
    plot(cseg, linewidth=2, marker='d', color=random_color(),
         label='{0}'.format(Contour(cseg).cseg_visual_printing()))
    title(title_name, family='georgia', size='small')
    legend(prop=FontProperties(size=12))
    show()


def multi_plot_preview(cseg_array):
    """Generates multiple cseg plot.

    [cseg, color]
    >>> multi_plot_preview([[[0, 2, 1], 'blue'], [[0, 1, 2], 'lightblue'],
                            [[0, 2, 3], 'green']])
    """

    csegs = [cseg for cseg, color in cseg_array]
    all_cps = flatten(csegs)

    cseg_yticks = range((min(all_cps)), (max(all_cps) + 1))
    cseg_xticks = range(max([len(x) for x in csegs]))

    fig = figure()
    fig.canvas.set_window_title(program_name)

    grid(color='b', linestyle='-', linewidth=.1)
    axis()

    title_name = program_name + " --- Contour plotter"
    xlabel('c-pitch position')
    ylabel('c-pitch')
    xticks(cseg_xticks)
    yticks(cseg_yticks)
    for cseg, color in cseg_array:
        plot(cseg, linewidth=2, color=color,
             label='{0}'.format(Contour(cseg).cseg_visual_printing()))

    title(title_name, family='georgia', size='small')
    legend(prop=FontProperties(size=12))
    show()
