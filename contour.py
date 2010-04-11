#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function


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
