#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contour

def fuzzy_membership(els):
    """Returns Fuzzy membership value. 1 if (cps1, cps2) is element of
    ascent contours, 0, if not.

    >>> fuzzy_membership(1, 3)
    1
    """

    if els[1] - els[0] > 0:
        return 1
    else:
        return 0


def fuzzy_comparison(els):
    """Returns fuzzy comparison.

    >>> fuzzy_comparison(3, 1)
    -1
    """

    retrograde_els = els[:]
    retrograde_els.reverse()
    return fuzzy_membership(els) - fuzzy_membership(retrograde_els)


def fuzzy_membership_matrix(cseg):
    """Returns fuzzy membership matrix.

    >>> fuzzy_membership_matrix(Contour([0, 2, 1]))
    [[0, 1, 1], [0, 0, 0], [0, 1, 0]]
    """

    size = len(cseg)
    r_size = range(size)
    m = [[a, b] for a in cseg for b in cseg]
    n = [m[(i * size):((i + 1) * size)] for i in range(size)]
    line = []
    [line.append([fuzzy_membership(x) for x in n[r]]) for r in r_size]
    return line


def fuzzy_comparison_matrix(cseg):
    """Returns fuzzy comparison matrix.

    >>> fuzzy_membership_matrix(Contour([0, 2, 1]))
    [[0, 1, 1], [0, 0, 0], [0, 1, 0]]
    """

    size = len(cseg)
    r_size = range(size)
    m = [[a, b] for a in cseg for b in cseg]
    n = [m[(i * size):((i + 1) * size)] for i in range(size)]
    line = []
    [line.append([fuzzy_comparison(x) for x in n[r]]) for r in r_size]
    return line
