#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pylab import grid, axis, plot, title, legend, show, xticks, yticks, \
     figure, ylabel, xlabel, axes, pie, imshow, rcParams, subplot
from matplotlib.font_manager import FontProperties
from PIL import Image

from contour import Contour
from utils import flatten
import random

program_name = "Villa Lobos Contour Module v.0.1"


def random_color():
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    return colors[random.randint(0, len(colors) - 1)]


def aux_plot(cseg):
    """Returns cseg plot data to plot.

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
    p = plot(cseg, linewidth=2, marker='d', color=random_color(),
         label='{0}'.format(Contour(cseg).cseg_visual_printing()))
    title(title_name, family='georgia', size='small')
    legend(prop=FontProperties(size=12))
    return p


def plot_preview(cseg):
    """Generates cseg plot.

    The code is based on
    http://matplotlib.sourceforge.net/examples/pylab_examples/unicode_demo.html

    >>> plot_preview([5, 3, 4, 1, 2, 0])
    """
    aux_plot(cseg)
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


def pie_plot(data, plot_title=""):
    ax = axes([0.1, 0.1, 0.8, 0.8])
    figure(1, figsize=(6, 6))
    title(plot_title, bbox={'facecolor': '0.8', 'pad': 5})
    sorted_data = sorted(data, key=lambda x: x[1])
    fracs = [x[1] for x in sorted_data]
    labels = [x[0] for x in sorted_data]

    pie(fracs,  labels=labels, autopct='%1.1f%%', shadow=True)
    show()

def cseg_pie_plot(data, plot_title=""):
    ax = axes([0.1, 0.1, 0.8, 0.8])
    figure(1, figsize=(6, 6))
    title(plot_title, bbox={'facecolor': '0.8', 'pad': 5})
    sorted_data = sorted(data, key=lambda x: x[1])
    fracs = [x[1] for x in sorted_data]
    labels = [Contour(x[0]).cseg_visual_printing() for x in sorted_data]

    pie(fracs,  labels=labels, autopct='%1.1f%%', shadow=True)
    show()

def aux_pdf(file):
    pdf = Image.open(file)
    dpi = rcParams['figure.dpi']
    figsize = pdf.size[0]/dpi, pdf.size[1]/dpi
    figure(figsize=figsize)
    ax = axes([0,0,1,1], frameon=False)
    ax.set_axis_off()
    return imshow(pdf, origin='lower')
