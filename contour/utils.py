#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess


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
        print("{0} - {1} %".format(n[0], n[1]))


def item_count(data):
    """Counts items in a list of lists"""

    sorted_subsets = sorted(data)
    tuples = [tuple(x) for x in sorted_subsets]
    contour_type = list(set(tuples))
    counted_contours = [[x, tuples.count(x)] for x in contour_type]
    return sorted(counted_contours, key=lambda x: x[1], reverse=True)


def abcm2ps(path, abc_filename):
    filename = abc_filename.split(".abc")[0]
    abc_file = path + "/" + abc_filename
    ps_file = path + "/" + filename + ".ps"
    subprocess.call('abcm2ps -O {0} {1}'.format(ps_file, abc_file), shell=True)

def double_replace(string):
    """Replaces -1 by -, and 1 by +. Accepts string as input."""

    return string.replace("-1", "-").replace("1", "+")


def replace_list_to_plus_minus(list):
    """Convert a list in a string and replace -1 by -, and 1 by +"""

    return " ".join([double_replace(str(x)) for x in list])


def replace_plus_minus_to_list(string):
    """Convert a string with - and + to a list with -1, and 1.

    >>> replace_plus_minus_to_list(\"- + -\")
    [-1, 1, -1]]
    >>> replace_plus_minus_to_list(\"-1 1 - + -\")
    [-1, 1, -1, 1, -1]]
    """

    partial1 = string.replace('-1', '-').replace('1', '+')
    partial2 = partial1.replace('-', '-1').replace('+', '1')
    return [int(x) for x in partial2.split(" ") if x]


def list_to_string(list):
    """Convert a list in a string.

    Inputs [1, 2, 3] and outputs '1 2 3'
    """

    return " ".join([str(x) for x in list])


def remove_duplicate_tuples(list_of_tuples):
    """Removes tuples that the first item is repeated in adjacent
    tuples. The removed tuple is the second."""

    prev = None
    tmp = []
    for a, b in list_of_tuples:
        if a != prev:
            tmp.append((a, b))
            prev = a
    return tmp
