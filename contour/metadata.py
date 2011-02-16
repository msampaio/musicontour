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


def __source_figure_add(filename):

    im = Image.open(filename)

    source_key = contour_key_creator("Source")
    figure_key = contour_key_creator("Figure")

    source, figure = get_source(filename)

    ## inserts source and figure automatically
    im.info[source_key] = source
    im.info[figure_key] = figure

    __pngsave(im, filename)


def add(filename, m_key, m_value, available_keys = keys):
    """Inserts metadata to a PNG file:

    >>> metadata.add('/tmp/foo.png', 'Page', '227')
    """
    if m_key in available_keys:
        im = Image.open(filename)

        __source_figure_add(filename)
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


def add_from_doc(data_file, path_to_figures):
    """Adds metadata collected in a data_file. The data_file must be
    written in this way:

    Contour_Source: marvin.ea87:relating
    Contour_Page: 227
    Contour_Figure: 1a
    Contour_Cseg: 9 8 7 8 6 5 4 3 2 1 0
    Contour_Caption: Same-Contour Melodies. Berg: Lyric Suite, (mvt. 11), vln. I, mrn. 66-67 and 72-73
    Contour_Description: The figure illustrates melodic patterns that share melodic contour but not set-class

    There is a empty line between figure data.

    >>> add_from_doc('/tmp/music_examples_database.txt', '/tmp/figs')
    """

    with open(data_file, "r") as f:
        data = f.read().split('\n\n')

        for figure_data in data:

            figure_data = figure_data.split('\n')
            figure_data_dic = {}

            for figure_item in figure_data:
                splitted = figure_item.split(' ')
                key = splitted[0].strip(':')
                value = " ".join(splitted[1:])

                if key:
                    figure_data_dic[key] = value

            source = figure_data_dic['Contour_Source']
            figure = figure_data_dic['Contour_Figure']
            figure_name = ".".join([source, figure])
            filename = path_to_figures + "/" + figure_name + ".png"

            im = Image.open(filename)

            for key in figure_data_dic.keys():
                im.info[key] = figure_data_dic[key]

            __pngsave(im, filename)


def pretty_data_view(filename):
    """Prints metadata in google docs file order.

    >>> metadata.pretty_data_view(''/tmp/marvin.ea87:relating.17-4.png')
    Contour_Source: marvin.ea87:relating
    Contour_Page: 252
    Contour_Figure: 17-4
    Contour_Cseg: 2 0 1 0 3
    Contour_Caption: Secondary Melodic Material: Webern, op. 10/1. Contour H: mm. 8-9
    Contour_Description:
    """

    dictionary = show(filename)

    for key in ["Contour_Source", "Contour_Page", "Contour_Figure",
                "Contour_Cseg", "Contour_Caption", "Contour_Description"]:

        if key not in dictionary:
            value = ""
        else:
            value = dictionary[key]

        print("{0}: {1}".format(key, value))
