#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess
import itertools

def flatten(seq):
    """Flatten Sequences."""

    return [item for sublist in seq for item in sublist]


def contour_class(contour_list):
    """Returns the contour class of a given contour."""

    sorted_contour = sorted(list(set(contour_list)))
    return [sorted_contour.index(x) for x in contour_list]


def absolute_subsets(contour, n):
    """Returns adjacent n-elements subsets of a given contour."""

    return [contour[i:i + n] for i in range((len(contour) - (n - 1)))]


def contour_subsets(contour, n):
    """Returns adjacent n-elements subsets of the contour class of a
    given contour."""

    return [contour_class(contour[i:n + i])
            for i in range((len(contour) - (n - 1)))]


def item_count(data):
    """Counts items in a list of lists"""

    sorted_subsets = sorted(data)
    tuples = [tuple(x) for x in sorted_subsets]
    contour_type = list(set(tuples))
    counted_contours = [[x, tuples.count(x)] for x in contour_type]
    return sorted(counted_contours, key=lambda x: x[1], reverse=True)


def contours_count(contour, n):
    """Counts contour subset classes with n elements."""

    sorted_subsets = sorted(contour_subsets(contour, n))
    tuples = [tuple(x) for x in sorted_subsets]
    contour_type = list(set(tuples))
    counted_contours = [[x, tuples.count(x)] for x in contour_type]
    return sorted(counted_contours, key=lambda x: x[1], reverse=True)


def extract_spine(filename, voice):
    """Extracts a spine from a kern file."""

    spine = subprocess.Popen('extractx -i %s %s' % (voice, filename),
                             stdout=subprocess.PIPE, shell=True)
    return spine.stdout.read()


def kern_file_process(path, basename, voice='*Ibass'):
    """Outputs frequency values."""

    cm1 = subprocess.Popen('extractx -i \'%s\' \"%s\"' % (voice,
                                                          path + basename + ".krn"),
                           stdout=subprocess.PIPE, shell=True)
    cm2 = subprocess.Popen('ditto', stdin=cm1.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cm3 = subprocess.Popen('sed \'s/^\[//g\'', stdin=cm2.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cm4 = subprocess.Popen('sed \'s/^[0-9].*\]//g\'', stdin=cm3.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cm5 = subprocess.Popen('sed \'s/[LJ;_]//g\'', stdin=cm4.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cm6 = subprocess.Popen('sed \'s/^[1248]//g\'', stdin=cm5.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cm7 = subprocess.Popen('sed \'s/^\.//g\'', stdin=cm6.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cm8 = subprocess.Popen('freq', stdin=cm7.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cm9 = subprocess.Popen('sed \'s/^\.//g\'', stdin=cm8.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cm10 = subprocess.Popen('rid -GLId', stdin=cm9.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cm11 = subprocess.Popen('egrep -v \"=|r\"', stdin=cm10.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cm12 = subprocess.Popen('uniq', stdin=cm11.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cm13 = subprocess.Popen('sed \'/^$/d\'', stdin=cm12.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cm14 = subprocess.Popen('sed \'s/X$//g\'', stdin=cm13.stdout,
                           stdout=subprocess.PIPE, shell=True)
    cmd = cm13
    subprocess.Popen('mkdir -p /tmp/freq', shell=True)
    with open("/tmp/freq/" + basename + '.freq', "w") as g:
        print(cmd.stdout.read(), file=g)


def freq_list(filename):
    """Outputs frequency in a list."""

    return [float(l) for l in file(filename)]


def contour_class_file(path, file_name):
    """Outputs contours classes from a frequency file."""

    complete_file = path + file_name
    return file_name, contour_class(freq_list(complete_file))


def frequency_file_contour_count(path, file_name, contour_size):
    """Outputs counted contours in a frequency file."""

    contour_classes = contour_class_file(path, file_name)[1]
    contour_counted = contours_count(contour_classes, contour_size)
    return file_name, contour_size, contour_counted


def percent(list):
    """Outputs percentuals from a list like [[(1, 0), 10],
    [(0, 1), 11]]"""

    sigma = sum(x[1] for x in list)
    return [[n[0], "%.2f" % (float(n[1]) * 100 / sigma)] for n in list]


def count_contours_list_of_files(path, list_of_files, n):
    """Count contour types in a list of frequency files in a same
    directory."""

    subsets = contour_class_file(path, file_name)[1]
    a = [contour_subsets(subsets, n) for file_name in list_of_files]
    return item_count(flatten(a))


def lists_printing(list):
    """Prints a list of two items lists."""

    for n in list:
        print("%s - %s %%" % (n[0], n[1]))
