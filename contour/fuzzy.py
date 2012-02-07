#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contour

def membership(els):
    """Returns Fuzzy membership value. 1 if (cps1, cps2) is element of
    ascent contours, 0, if not.

    >>> fuzzy_membership(1, 3)
    1
    """

    if els[1] - els[0] > 0:
        return 1
    else:
        return 0


def comparison(els):
    """Returns fuzzy comparison.

    >>> fuzzy_comparison(3, 1)
    -1
    """

    retrograde_els = els[:]
    retrograde_els.reverse()
    return membership(els) - membership(retrograde_els)


class FuzzyMatrix(list):
    """Returns an objcect comparison matrix.
    Input is a list of lists, each of them representing a line in
    matrix:

    >>> FuzzyMatrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]])
    """

    def diagonal(self, n=1):

        if n < len(self):
            diagonal_size = len(self) - n
            return [self[x][x + n] for x in range(diagonal_size)]

    def superior_triangle(self, n=1):

        if n < len(self):
            return [line[i + n:] for i, line in enumerate(self) if line][:-n]

    def __repr__(self):

        return "\n".join([" ".join([str(row) for row in line]) for line in self])

