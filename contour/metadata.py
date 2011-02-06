#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from PIL import Image


metadata_keys = set(["Contour_Source", "Contour_Page", "Contour_Figure",
                     "Contour_Caption", "Contour_Description",
                     "Contour_Cseg"])


def pngsave(im, file):
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


def add(filename, m_key, m_value, available_keys = metadata_keys):
    """Inserts metadata to a PNG file:

    >>> metadata_add('/tmp/foo.png', 'Contour_Source', 'marvin.ea87:relating')
    """

    if m_key in available_keys:
        im = Image.open(filename)
        im.info[m_key] = m_value
        pngsave(im, filename)
    else:
        print("Selected m_key '{0}' is not one of the available keys list:\n".format(m_key))
        for key in sorted(list(available_keys)):
            print("{0}".format(key))


def remove(filename, m_key):
    """Removes metadata from a PNG file:

    >>> metadata_remove('/tmp/foo.png', 'Contour_Source')
    """

    im = Image.open(filename)
    if m_key in im.info: del im.info[m_key]
    pngsave(im, filename)


def show(filename):
    """Shows metadata in a PNG file:

    >>> metadata_add('/tmp/foo.png')
    {'Contour_Source': 'marvin.ea87:relating'}
    """

    im = Image.open(filename)
    return im.info
