#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


def contour_class(contour_list):
    sorted_contour = sorted(list(set(contour_list)))
    return [sorted_contour.index(x) for x in contour_list]


def absolute_subsets(contour, n):
    return [contour[i:i+n] for i in range((len(contour) - n))]


def contour_subsets(contour, n):
    return [contour_class(contour[i:n+i])
            for i in range((len(contour) - n))]


def contours_count(contour, n):
    '''Counts contour subset classes with n elements.'''
    sorted_subsets = sorted(contour_subsets(contour, n))
    tuples = [tuple(x) for x in sorted_subsets]
    contour_type = list(set(tuples))
    counted_contours = [[x, tuples.count(x)] for x in contour_type]
    return sorted(counted_contours, key=lambda x: x[1], reverse=True)


### data
## soprano, choral 002
contour = [440.00, 493.88, 392.00, 369.99, 329.63, 493.88, 554.37,
493.88, 440.00, 415.30, 369.99, 415.30, 369.99, 329.63, 659.26,
587.33, 554.37, 493.88, 440.00, 493.88, 554.37, 493.88, 554.37,
587.33, 554.37, 493.88, 466.16, 493.88, 329.63, 440.00, 493.88,
554.37, 587.33, 659.26, 587.33, 554.37, 493.88, 587.33, 554.37,
493.88, 659.26, 587.33, 554.37, 493.88, 440.00, 493.88, 554.37,
493.88, 440.00]


contour_cc = contour_class(contour)


print(contours_count(contour_cc, 4))
