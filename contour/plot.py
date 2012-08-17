#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab
import matplotlib
import PIL
from PIL import Image
from PIL import ImageChops
import random
import matplotlib.pyplot as pyplot
from matplotlib.ticker import MultipleLocator


name = "MusiContour"
version = "0.3"
program_name = "{0} v.{1}".format(name, version)


def _contour_lines(obj_cseg, plot_color, custom_legend=""):
    """Returns cseg plot data to plot.

    The code is based on
    http://matplotlib.sourceforge.net/examples/pylab_examples/unicode_demo.html
    """

    matplotlib.rcParams.update({'font.size': 14,
                                'lines.linewidth': 3,
                                'lines.linestyle': '-',
                                'lines.marker': 'o',
                                'figure.figsize': (5, 5),
                                'grid.color': '0.7',
                                'grid.linewidth': 0.1,
                                'grid.linestyle': '-',
                                'xtick.minor.size': 1,
                                'xtick.major.size': 1,
                                })

    title_name = program_name + " - Contour plotter"

    fig = pylab.figure(num=1)
    ax = fig.add_subplot(111)
    pylab.grid()
    ax.xaxis.set_major_locator(MultipleLocator(1.0))
    ax.yaxis.set_major_locator(MultipleLocator(1.0))

    pylab.xlabel('c-point position')
    pylab.ylabel('c-point value')

    pylab.title(title_name, family='georgia', size='small')

    if custom_legend == None:
        p = ax.plot(obj_cseg.positions, obj_cseg.cseg, color=plot_color)
    else:
        p = ax.plot(obj_cseg.positions, obj_cseg.cseg, color=plot_color, label='{0} {1}'.format(obj_cseg, custom_legend))
        ax.legend(loc='best')

    return p


def clear():
    """Clear plot image."""

    pylab.clf()


def contour_lines(*obj_csegs):
    """Generates cseg plot.

    The code is based on
    http://matplotlib.sourceforge.net/examples/pylab_examples/unicode_demo.html

    For one contour:
    >>> contour([Contour([5, 3, 4, 1, 2, 0]), '\#006633', 'contour legend'])

    For multiple contours:
    >>> c1 = Contour([1, 3, 0, 2])
    >>> c2 = Contour([2, 0, 3, 1])
    >>> contour([c1, 'g', 'main contour'], [c2, 'b', 'secondary contour'])
    """

    for [obj_cseg, plot_color, legend] in obj_csegs:
        _contour_lines(obj_cseg, plot_color, legend)
    pylab.show()


def contour_lines_save_multiple(*obj_csegs):
    """Saves csegs graphs in a svg format file for each cseg.

    >>> c1 = Contour([1, 3, 0, 2])
    >>> c2 = Contour([2, 0, 3, 1])
    >>> contour([c1, 'g', 'main contour'], [c2, 'b', 'secondary contour'])
    """

    for [obj_cseg, plot_color, legend] in obj_csegs:
        clear()
        _contour_lines(obj_cseg, plot_color, legend)
        filename = ''.join([str(x) for x in obj_cseg.cseg])
        pyplot.savefig(filename + '.svg')


def contour_lines_save_unique(*obj_csegs):
    """Saves csegs graphs in a unique svg format file for all csegs.

    >>> c1 = Contour([1, 3, 0, 2])
    >>> c2 = Contour([2, 0, 3, 1])
    >>> contour([c1, 'g', 'main contour'], [c2, 'b', 'secondary contour'])
    """

    clear()
    for [obj_cseg, plot_color, legend] in obj_csegs:
        _contour_lines(obj_cseg, plot_color, legend)

    pyplot.savefig('cseg_output.svg')


def contour_lines_save_django(filename, *obj_csegs):
    """Saves csegs graphs in a unique svg format file for all csegs.

    >>> c1 = Contour([1, 3, 0, 2])
    >>> c2 = Contour([2, 0, 3, 1])
    >>> contour_lines_save_django([c1, 'g', 'C1'], [c2, 'b', 'C2'])
    """

    clear()
    for [obj_cseg, plot_color, legend] in obj_csegs:
        _contour_lines(obj_cseg, plot_color, legend)

    pyplot.savefig(filename, dpi=80)


def pie(data, plot_title=""):
    ax = pylab.axes([0.1, 0.1, 0.8, 0.8])
    pylab.figure(1, figsize=(6, 6))
    pylab.title(plot_title, bbox={'facecolor': '0.8', 'pad': 5})
    sorted_data = sorted(data, key=lambda x: x[1])
    fracs = [x[1] for x in sorted_data]
    labels = [x[0] for x in sorted_data]
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'w']

    pylab.pie(fracs, colors=colors, labels=labels, autopct='%1.1f%%', shadow=True)
    pylab.show()


def pie_comparison(data, plot_title=""):
    ax = pylab.axes([0.1, 0.1, 0.8, 0.8])
    pylab.figure(1, figsize=(6, 6))
    pylab.title(plot_title, bbox={'facecolor': '0.8', 'pad': 5})
    sorted_data = sorted(data, key=lambda x: x[1])
    fracs = [x[1] for x in sorted_data]
    labels = [contour.Contour(x[0]) for x in sorted_data]

    pylab.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=True)
    pylab.show()


def _autoCrop(image, backgroundColor=None):
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
        raise NotImplementedError("Sorry, this function is not " + \
              "implemented yet for images in mode '{0}'.".format(image.mode))

    if bbox:
        image = image.crop(bbox)

    return image


def _pdf(file):
    img = Image.open(file)
    pdf = _autoCrop(img)
    im = pylab.imshow(pdf, origin='lower')
    return im


def contour_line_score(obj_cseg, file, plot_color="k"):
    pylab.subplot(212)
    _pdf(file)

    pylab.subplot(211)
    _contour_lines(obj_cseg, plot_color)

    pylab.show()
