#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab as pl

def plot_preview(cseg):
    """Generates cseg plot.

    The code is based on
    http://matplotlib.sourceforge.net/examples/pylab_examples/unicode_demo.html
    """

    pl.plot(cseg)
    pl.title("Contour segment {0}".format(cseg))
    pl.show()
