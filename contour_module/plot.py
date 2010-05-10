#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pylab import (grid, axis, plot, title, legend, show, xticks,
     yticks, figure, ylabel, xlabel, axes, pie, imshow, rcParams,
     subplot, clf)
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import NullLocator
from PIL import (Image, ImageChops)

from contour import Contour
from utils import flatten
import random

program_name = "Villa-Lobos Contour Module v.0.1"


def random_color():
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    return colors[random.randint(0, len(colors) - 1)]


def aux_plot(cseg, plot_color, custom_legend=""):
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
    p = plot(cseg, linewidth=2, marker='d', color=plot_color,
         label='{0} {1}'.format(Contour(cseg).str_print(), custom_legend))
    title(title_name, family='georgia', size='small')
    legend(prop=FontProperties(size=10))
    return p


def plot_preview(cseg, plot_color, legend=""):
    """Generates cseg plot.

    The code is based on
    http://matplotlib.sourceforge.net/examples/pylab_examples/unicode_demo.html

    >>> plot_preview([5, 3, 4, 1, 2, 0])
    """

    aux_plot(cseg, plot_color, legend)
    show()


def clear_plot():
    """Clear plot image."""

    clf()


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
             label='{0}'.format(Contour(cseg).str_print()))

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
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'w']

    pie(fracs, colors=colors, labels=labels, autopct='%1.1f%%', shadow=True)
    show()


def cseg_pie_plot(data, plot_title=""):
    ax = axes([0.1, 0.1, 0.8, 0.8])
    figure(1, figsize=(6, 6))
    title(plot_title, bbox={'facecolor': '0.8', 'pad': 5})
    sorted_data = sorted(data, key=lambda x: x[1])
    fracs = [x[1] for x in sorted_data]
    labels = [Contour(x[0]).str_print() for x in sorted_data]

    pie(fracs,  labels=labels, autopct='%1.1f%%', shadow=True)
    show()


def autoCrop(image, backgroundColor=None):
    '''Intelligent automatic image cropping.
       This functions removes the usless "white" space around an image.


       If the image has an alpha (tranparency) channel, it will be used
       to choose what to crop.


       Otherwise, this function will try to find the most popular color
       on the edges of the image and consider this color "whitespace".
       (You can override this color with the backgroundColor parameter)


       Input:
            image (a PIL Image object): The image to crop.
            backgroundColor (3 integers tuple): eg. (0,0,255)
                 The color to consider "background to crop".
                 If the image is transparent, this parameters will be ignored.
                 If the image is not transparent and this parameter is not
                 provided, it will be automatically calculated.


       Output:
            a PIL Image object : The cropped image.


       From: http://sebsauvage.net/python/snyppets/#autocrop
    '''

    def mostPopularEdgeColor(image):
        ''' Compute who's the most popular color on the edges of an image.
            (left,right,top,bottom)

            Input:
                image: a PIL Image object

            Ouput:
                The most popular color (A tuple of integers (R,G,B))
        '''
        im = image
        if im.mode != 'RGB':
            im = image.convert("RGB")

        # Get pixels from the edges of the image:
        width, height = im.size
        left = im.crop((0, 1, 1, height - 1))
        right = im.crop((width - 1, 1, width, height - 1))
        top = im.crop((0, 0, width, 1))
        bottom = im.crop((0, height - 1, width, height))
        pixels = left.tostring() + right.tostring() + top.tostring() + bottom.tostring()

        # Compute who's the most popular RGB triplet
        counts = {}
        for i in range(0, len(pixels), 3):
            RGB = pixels[i] + pixels[i + 1] + pixels[i + 2]
            if RGB in counts:
                counts[RGB] += 1
            else:
                counts[RGB] = 1

        # Get the colour which is the most popular:
        mostPopularColor = sorted([(count, rgba) for (rgba, count) in counts.items()], reverse=True)[0][1]
        return ord(mostPopularColor[0]), ord(mostPopularColor[1]), ord(mostPopularColor[2])

    bbox = None

    # If the image has an alpha (tranparency) layer, we use it to crop the image.
    # Otherwise, we look at the pixels around the image (top, left, bottom and right)
    # and use the most used color as the color to crop.

    # --- For transparent images -----------------------------------------------
    if 'A' in image.getbands():  # If the image has a transparency layer, use it.
        # This works for all modes which have transparency layer
        bbox = image.split()[list(image.getbands()).index('A')].getbbox()
    # --- For non-transparent images -------------------------------------------
    elif image.mode == 'RGB':
        if not backgroundColor:
            backgroundColor = mostPopularEdgeColor(image)
        # Crop a non-transparent image.
        # .getbbox() always crops the black color.
        # So we need to substract the "background" color from our image.
        bg = Image.new("RGB", image.size, backgroundColor)
        diff = ImageChops.difference(image, bg)  # Substract background color from image
        bbox = diff.getbbox()  # Try to find the real bounding box of the image.
    else:
        raise NotImplementedError, "Sorry, this function is not " + \
              "implemented yet for images in mode '{0}'.".format(image.mode)

    if bbox:
        image = image.crop(bbox)

    return image


def aux_pdf(file):
    img = Image.open(file)
    pdf = autoCrop(img)
    im = imshow(pdf, origin='lower')
    return im


def plot_cseg_and_pdf(cseg, file):
    subplot(212)
    aux_pdf(file)

    subplot(211)
    aux_plot(cseg)

    show()
