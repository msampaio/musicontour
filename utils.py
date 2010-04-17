#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


def flatten(seq):
    """Flatten Sequences."""

    return [item for sublist in seq for item in sublist]


def filter_int(item):
    """Tests and outputs int."""

    if isinstance(item, int):
        return item
    else:
        return ''


def percent(list):
    """Outputs percentuals from a list like [[(1, 0), 10],
    [(0, 1), 11]]"""

    sigma = sum(x[1] for x in list)
    return [[n[0], "%.2f" % (float(n[1]) * 100 / sigma)] for n in list]


def lists_printing(list):
    """Prints a list of two items lists."""

    for n in list:
        print("{0} - {1} %%".format(n[0], n[1]))


def item_count(data):
    """Counts items in a list of lists"""

    sorted_subsets = sorted(data)
    tuples = [tuple(x) for x in sorted_subsets]
    contour_type = list(set(tuples))
    counted_contours = [[x, tuples.count(x)] for x in contour_type]
    return sorted(counted_contours, key=lambda x: x[1], reverse=True)
