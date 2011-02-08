#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from PIL import Image
import os


keys = set(["Source", "Page", "Figure", "Caption", "Description", "Cseg"])


def __pngsave(im, file):
    # source: http://blog.client9.com/2007/08/python-pil-and-png-metadata-take-2.html
    # these can be automatically added to Image.info dict
    # they are not user-added metadata
    reserved = ('interlace', 'gamma', 'dpi', 'transparency', 'aspect')

    # undocumented class
    from PIL import PngImagePlugin
    meta = PngImagePlugin.PngInfo()

    # copy metadata into new object
    for k,v in im.info.iteritems():
        if k in reserved: continue
        meta.add_text(k, v, 0)

    # and save
    im.save(file, "PNG", pnginfo=meta)


def contour_key_creator(string):
    """Concatenates contour metadata with prefix 'Contour_'.

    >>> metadata.contour_key_creator('Page')
    Contour_Page
    """

    return "Contour_" + string


def get_source(abs_filename):
    """Returns source and figure number from absolute filename:

    >>> metadata.get_source('/tmp/sampaio08:torno.2b.png')
    ('sampaio08:torno', '2b')
    """

    filename = os.path.basename(abs_filename)
    splitted = filename.split(".")
    figure = splitted[-2]
    source = ".".join(splitted[:-2])

    return source, figure


def add(filename, m_key, m_value, available_keys = keys):
    """Inserts metadata to a PNG file:

    >>> metadata.add('/tmp/foo.png', 'Page', '227')
    """

    source_key = contour_key_creator("Source")
    figure_key = contour_key_creator("Figure")

    source, figure = get_source(filename)

    if m_key in available_keys:
        im = Image.open(filename)

        ## inserts source and figure automatically
        im.info[source_key] = source
        im.info[figure_key] = figure

        im.info[contour_key_creator(m_key)] = m_value
        __pngsave(im, filename)

    else:
        print("Selected m_key '{0}' is not one of the available keys list:\n".format(m_key))
        for key in sorted(list(available_keys)):
            print("{0}".format(key))


def remove(filename, m_key):
    """Removes metadata from a PNG file:

    >>> metadata.remove('/tmp/foo.png', 'Description')
    """

    complete_key = contour_key_creator(m_key)
    im = Image.open(filename)
    if complete_key in im.info: del im.info[complete_key]
    __pngsave(im, filename)


def show(filename):
    """Shows metadata in a PNG file:

    >>> metadata.show('/tmp/foo.png')
    {'Contour_Source': 'marvin.ea87:relating', 'Contour_Figure': '2b'}
    """

    im = Image.open(filename)
    return im.info
