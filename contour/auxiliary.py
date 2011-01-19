#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import itertools
import contour


def permut_csegs(cardinality):
    """Returns a list of possible normalized csegs of a given
    cardinality."""

    base = range(cardinality)
    return sorted(itertools.permutations(base, cardinality))


def subsets_count(subsets_list):
    """Counts contour subset classes with n elements."""

    tuples = [tuple(x) for x in subsets_list]
    contour_type = sorted(list(set(tuples)))
    counted_contours = [[x, tuples.count(x)] for x in contour_type]
    return sorted(counted_contours, key=lambda x: x[1], reverse=True)


def normal_form_subsets(subsets_list):
    """Outputs normal form of a list of subsets."""

    return [contour.Contour(x).translation() for x in subsets_list]


def prime_form_subsets(subsets_list):
    """Outputs normal form of a list of subsets."""

    return [contour.Contour(x).prime_form() for x in subsets_list]


def normal_form_subsets_count(subsets_list):
    """Counts subset prime forms with n elements."""

    normal_form = normal_form_subsets(subsets_list)
    return subsets_count(normal_form)


def prime_form_subsets_count(subsets_list):
    """Counts subset prime forms with n elements."""

    prime_form = prime_form_subsets(subsets_list)
    return subsets_count(prime_form)


def apply_fn(cseg, fn):
    """Apply a method to a contour."""

    return apply(getattr(contour.Contour(cseg), fn))
