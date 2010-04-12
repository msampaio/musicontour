#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess


def merge(seq):
    '''Merge Sequences.'''
    merged = []
    for s in seq:
        for x in s:
            merged.append(x)
    return merged


def contour_class(contour_list):
    '''Returns the contour class of a given contour.'''
    sorted_contour = sorted(list(set(contour_list)))
    return [sorted_contour.index(x) for x in contour_list]


def absolute_subsets(contour, n):
    '''Returns adjacent n-elements subsets of a given contour.'''
    return [contour[i:i + n] for i in range((len(contour) - (n - 1)))]


def contour_subsets(contour, n):
    '''Returns adjacent n-elements subsets of the contour class of a
    given contour.'''
    return [contour_class(contour[i:n + i])
            for i in range((len(contour) - (n - 1)))]


def item_count(data):
    '''Counts items in a list of lists'''
    sorted_subsets = sorted(data)
    tuples = [tuple(x) for x in sorted_subsets]
    contour_type = list(set(tuples))
    counted_contours = [[x, tuples.count(x)] for x in contour_type]
    return sorted(counted_contours, key=lambda x: x[1], reverse=True)


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


def contour_class_file(path, file_name):
    '''Outputs contours classes from a frequency file.'''
    complete_file = path + file_name
    frequency = freq_process(complete_file)
    contour_classes = contour_class(frequency)
    return file_name, contour_classes


def frequency_file_contour_count(path, file_name, contour_size):
    '''Outputs counted contours in a frequency file.'''
    contour_classes = contour_class_file(path, file_name)[1]
    contour_counted = contours_count(contour_classes, contour_size)
    return file_name, contour_size, contour_counted


def percent(list):
    '''Outputs percentuals from a list like [[(1, 0), 10],
    [(0, 1), 11]]'''
    sigma = sum(x[1] for x in list)
    percent = [[n[0], "%.2f" % (float(n[1])* 100 / sigma)]
               for n in list]
    return percent


def count_contours_list_of_files(path, list_of_files, n):
    '''Count contour types in a list of frequency files in a same
    directory.'''
    a = [contour_subsets(contour_class_file(path, file_name)[1], n)
         for file_name in list_of_files]
    b = merge(a)
    result = item_count(b)
    return result
