#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess


def contour_class(contour_list):
    sorted_contour = sorted(list(set(contour_list)))
    return [sorted_contour.index(x) for x in contour_list]


def absolute_subsets(contour, n):
    return [contour[i:i + n] for i in range((len(contour) - n))]


def contour_subsets(contour, n):
    return [contour_class(contour[i:n + i])
            for i in range((len(contour) - n))]


def contours_count(contour, n):
    '''Counts contour subset classes with n elements.'''
    sorted_subsets = sorted(contour_subsets(contour, n))
    tuples = [tuple(x) for x in sorted_subsets]
    contour_type = list(set(tuples))
    counted_contours = [[x, tuples.count(x)] for x in contour_type]
    return sorted(counted_contours, key=lambda x: x[1], reverse=True)


def kern_file_process(filename, voice='*Isoprn'):
    '''Outputs frequency values.'''
    extract = subprocess.Popen('extractx -i %s %s'
                               % (voice, filename),
                               stdout=subprocess.PIPE, shell=True)
    sed = subprocess.Popen('sed \'s/[12468.JL;]//g\'',
                           stdin=extract.stdout,
                           stdout=subprocess.PIPE, shell=True)
    frequency = subprocess.Popen('freq', stdin=sed.stdout,
                                 stdout=subprocess.PIPE, shell=True)
    rid = subprocess.Popen('rid -GLId', stdin=frequency.stdout,
                                 stdout=subprocess.PIPE, shell=True)
    egrep = subprocess.Popen('egrep -v \"=|r\"', stdin=rid.stdout,
                                 stdout=subprocess.PIPE, shell=True)
    uniq = subprocess.Popen('uniq', stdin=egrep.stdout,
                                 stdout=subprocess.PIPE, shell=True)
    print(uniq.stdout.read())


def freq_process(filename):
    '''Outputs frequency in a list.'''
    lines = [float(l) for l in file(filename)]
    return lines
