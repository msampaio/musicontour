#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess as sp
import itertools
import pitch as p


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

    spine = sp.Popen('extractx -i {0} {1}'.format(voice, filename),
                             stdout=sp.PIPE, shell=True)
    return spine.stdout.read()


def humdrum_pitch(kern_file, voice):
    """Outputs **pitch from a kern file."""

    cmd1 = sp.Popen('extractx -i {0} {1}'.format(voice, kern_file),
                    stdout=sp.PIPE, shell=True)
    cmd2 = sp.Popen('pitch', stdin=cmd1.stdout,
                    stdout=sp.PIPE, shell=True)
    return cmd2.stdout.read()


def kern_file_process(path, basename, voice='*Ibass'):
    """Outputs frequency values."""

    cm1 = sp.Popen('extractx -i {0} {1}'.format(voice,
                                                path + basename + ".krn"),
                           stdout=sp.PIPE, shell=True)
    cm2 = sp.Popen('ditto', stdin=cm1.stdout,
                           stdout=sp.PIPE, shell=True)
    cm3 = sp.Popen('sed \'s/^\[//g\'', stdin=cm2.stdout,
                           stdout=sp.PIPE, shell=True)
    cm4 = sp.Popen('sed \'s/^[0-9].*\]//g\'', stdin=cm3.stdout,
                           stdout=sp.PIPE, shell=True)
    cm5 = sp.Popen('sed \'s/[LJ;_]//g\'', stdin=cm4.stdout,
                           stdout=sp.PIPE, shell=True)
    cm6 = sp.Popen('sed \'s/^[1248]//g\'', stdin=cm5.stdout,
                           stdout=sp.PIPE, shell=True)
    cm7 = sp.Popen('sed \'s/^\.//g\'', stdin=cm6.stdout,
                           stdout=sp.PIPE, shell=True)
    cm8 = sp.Popen('freq', stdin=cm7.stdout,
                           stdout=sp.PIPE, shell=True)
    cm9 = sp.Popen('sed \'s/^\.//g\'', stdin=cm8.stdout,
                           stdout=sp.PIPE, shell=True)
    cm10 = sp.Popen('rid -GLId', stdin=cm9.stdout,
                           stdout=sp.PIPE, shell=True)
    cm11 = sp.Popen('egrep -v \"=|r\"', stdin=cm10.stdout,
                           stdout=sp.PIPE, shell=True)
    cm12 = sp.Popen('uniq', stdin=cm11.stdout,
                           stdout=sp.PIPE, shell=True)
    cm13 = sp.Popen('sed \'/^$/d\'', stdin=cm12.stdout,
                           stdout=sp.PIPE, shell=True)
    cm14 = sp.Popen('sed \'s/X$//g\'', stdin=cm13.stdout,
                           stdout=sp.PIPE, shell=True)
    cmd = cm13
    sp.Popen('mkdir -p /tmp/freq', shell=True)
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
        print("{0} - {1} %%".format(n[0], n[1]))


def filter_int(item):
    """Tests and outputs int."""

    if isinstance(item, int):
        return item
    else:
        return ''


def contour_class_kern(lista):
    """Outputs contour class from a kern list."""

    lista = contour_class([filter_int(item)
                           for item in lista if filter_int(item)])
    return lista


def contour_class_one_function(path, krn_file, voice):
    """Outputs contour class in one single function."""

    hum_pitch = humdrum_pitch(path + krn_file, voice)
    parsed_kern = [p.parse_pitch(line) for line in hum_pitch.split('\n')]
    contour_class = contour_class_kern(parsed_kern)
    return contour_class

class Contour():

    def retrograde(self):
        """Returns contour retrograde."""
        
        self.elements.reverse()
        return self.elements


    def inversion(self):
        """Returns contour inversion."""

        maxim = max(self.elements)
        minim = min(self.elements)
        axis = (maxim - minim)/2
        return [((axis * 2) - x) for x in self.elements]


    def contour_class(self):
        """Returns the contour class of a given contour."""

        sorted_contour = sorted(list(set(self.elements)))
        return [sorted_contour.index(x) for x in self.elements]


    def prime_form(self):
        """Returns the contour class of a given contour."""

        length = len(self.elements)
        cc = self.contour_class(self.elements)
        if ((length - 1) - cc[-1]) < cc[0]:
            inv = self.inversion(cc)
        else:
            inv = cc
        if inv[-1] < inv[0]:
            ret = self.retrograde(inv)
        else:
            ret = inv
        return ret

    def __init__(self, list):
        self.elements = list
