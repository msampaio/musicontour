#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import contour as c
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.axislines import SubplotZero


def plot_cseg(cseg):
    """Generates cseg plot.

    The code is based on
    http://matplotlib.sourceforge.net/examples/axes_grid/simple_axisline.html
    """

    if 1:

        fig = plt.figure(1)
        fig.subplots_adjust(right=0.85)
        ax = SubplotZero(fig, 1, 1, 1)
        fig.add_subplot(ax)

        ax.plot(cseg)
        plt.draw()
        plt.show()
