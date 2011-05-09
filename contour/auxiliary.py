#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import itertools
import contour
import utils


def permut_csegs(cardinality):
    """Returns a list of possible normalized csegs of a given
    cardinality. Cseg are output as lists.

    >>> permut_csegs(3)
    [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
    """

    base = range(cardinality)
    return utils.permut_list(base)


def apply_fn(cseg, fn):
    """Apply a method to a contour.

    >>> apply_fn(Contour([0, 1, 2]), 'retrograde')
    < 2 1 0 >
    """

    return apply(getattr(contour.Contour(cseg), fn))


def absolute_pitches(cseg, pitch_set):
    """Returns absolute pitches for given cseg and pitch set with the
    same cardinality.

    >>> absolute_pitches(Contour([1, 4, 2, 3, 0]), [0, 7, 6, 9, 4])
    [12, 31, 18, 21, 4]
    """

    # lists stores [position, cpitch, pitch] for each pitch
    lists = [[pos, cseg[pos], value] for (pos, value) in enumerate(pitch_set)]
    lists = sorted(lists, key=lambda x: x[1])

    for el in range(1, len(lists)):
        interval = lists[el][2] - lists[el - 1][2]
        # increases octaves if interval between a pitch and previous
        # is negative
        if interval < 0:
            octave = abs(interval / 12) * 12
            lists[el] = [lists[el][0], lists[el][1], (lists[el][2] + octave)]
    return [x[2] for x in sorted(lists, key=lambda x: x[0])]


def absolute_pitches_permutation(cseg, psets_list):
    """Returns lists of absolute pitches permutations of a given cseg
    and a list of pitch sets permutations.

    >>> absolute_pitches_permutation(Contour([0, 1, 2]), [3, 4, 5])
    [[3, 4, 5], [3, 5, 16], [4, 15, 17], [4, 5, 15], [5, 15, 16], [5, 16, 27]]
    """

    permutted = utils.permut_list(psets_list)
    return [absolute_pitches(cseg, pset) for pset in permutted]


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


def interval(els):
    """Returns Friedmann (1985) CI, the distance between one
    element in a CC (normal_form cseg here), and a later element
    as signified by +, - and a number (without + here). For
    example, in cseg = [0, 2, 1], CI(0, 2) = 2, e CI(2, 1) = -1.
    """

    el1, el2 = els
    return el2 - el1

def comparison(els):
    """Returns Morris (1987) comparison [COM(a, b)] for two
    c-pitches.

    This function calls interval(), but in contour theory there is no
    relation between them. This calling reason is only to reduce code.
    """

    delta = interval(els)
    return 0 if abs(delta) == 0 else (delta) / abs(delta)
