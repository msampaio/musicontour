#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import itertools
import contour
import utils

def permut_csegs(cardinality):
    """Returns a list of possible normalized csegs of a given
    cardinality."""

    base = range(cardinality)
    return utils.permut_list(base)


def subsets_count(subsets_list):
    """Counts contour subset classes with n elements."""

    tuples = [tuple(x) for x in subsets_list]
    contour_type = sorted(list(set(tuples)))
    counted_contours = [[x, tuples.count(x)] for x in contour_type]
    return sorted(counted_contours, key=lambda x: x[1], reverse=True)


def normal_form_subsets(subsets_list):
    """Outputs normal form of a list of subsets."""

    return [contour.Contour(x).translation() for x in subsets_list]


def prime_form_subsets(subsets_list, prime_algorithm="prime_form_marvin_laprade"):
    """Outputs prime form of a list of subsets."""

    return [apply_fn(contour.Contour(x), prime_algorithm) for x in subsets_list]


def normal_form_subsets_count(subsets_list):
    """Counts subset normal forms with n elements."""

    normal_form = normal_form_subsets(subsets_list)
    return subsets_count(normal_form)


def prime_form_subsets_count(subsets_list, prime_algorithm="prime_form_marvin_laprade"):
    """Counts subset prime forms with n elements."""

    prime_form = prime_form_subsets(subsets_list, prime_algorithm)
    return subsets_count(prime_form)


def apply_fn(cseg, fn):
    """Apply a method to a contour."""

    return apply(getattr(contour.Contour(cseg), fn))


def absolute_pitches(cseg, pitch_set):
    """Returns absolute pitches for given cseg and pitch set with the
    same cardinality.

    >>> absolute_pitches(Contour([1, 4, 2, 3, 0]), [0, 7, 6, 9, 4])
    [12, 31, 18, 21, 4]
    """

    ## lists stores [position, cpitch, pitch] for each pitch
    lists = [[pos, cseg[pos], value] for (pos, value) in enumerate(pitch_set)]
    lists = sorted(lists, key = lambda x: x[1])

    for el in range(1, len(lists)):
        interval = lists[el][2] - lists[el - 1][2]
        ## increases octaves if interval between a pitch and previous
        ## is negative
        if interval < 0:
            octave = abs(interval / 12) * 12
            lists[el] = [lists[el][0], lists[el][1], (lists[el][2] + octave)]
    return [x[2] for x in sorted(lists, key = lambda x: x[0])]


def octave_calculator(pitch):
    """Returns pitch class and octave for a given absolute pitch.

    >>> octave_calculator(50)
    (2, 4)
    """

    p_class = pitch % 12
    octave = pitch / 12
    return (p_class, octave)


def cseg_string_to_Contour(cseg_string):
    """Returns a Contour object from a cseg string:

    >>> cseg_string_to_Contour('< 0 1 2 >')
    Contour([0, 1, 2])
    """

    splitted = cseg_string.strip("<").strip(">").split()

    return contour.Contour([int(x) for x in splitted])
