#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contour
import utils
import auxiliary
import numpy


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
        """Returns the matrix n diagonal.

        >>> FuzzyMatrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]]).diagonal()
        [1, -1]
        """

        if n < len(self):
            diagonal_size = len(self) - n
            return [self[x][x + n] for x in range(diagonal_size)]

    def superior_triangle(self, n=1):
        """Returns the matrix superior triangle from a given n
        diagonal.

        >>> FuzzyMatrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]]).superior_triangle()
        [[1, 1], [-1]]
        """

        if n < len(self):
            return [line[i + n:] for i, line in enumerate(self) if line][:-n]

    def except_zero_diagonal(self):
        """Returns the matrix without main zero diagonal.

        >>> FuzzyMatrix([[0, 1, 1, 1],
                         [0, 0, 1, 1],
                         [0, 0, 0, 0],
                         [0, 0, 1, 0]]).except_zero_diagonal()
        [[1, 1, 1], [0, 1, 1], [0, 0, 0], [0, 0, 1]]
        """

        return [[el for r, el in enumerate(line) if l != r] for l, line in enumerate(self)]

    def __repr__(self):

        return "\n".join([" ".join([str(row) for row in line]) for line in self])


def membership_similarity(cseg1, cseg2):
    """Returns similarity from a fuzzy membership matrix. Quinn 1997.

    >>> fuzzy.membership_similarity(Contour([4, 0, 1, 3, 2]), Contour([4, 1, 2, 3, 0]))
    0.8
    """

    fuzzy1 = utils.flatten(cseg1.fuzzy_membership_matrix().except_zero_diagonal())
    fuzzy2 = utils.flatten(cseg2.fuzzy_membership_matrix().except_zero_diagonal())

    return auxiliary.position_comparison(fuzzy1, fuzzy2)


def average_matrix(*csegs):
    """Returns the matrix of an average contour from a list of
    contours.

    >>> average_matrix(Contour([3, 0, 1, 2, 1]), Contour([4, 0, 1, 3, 2]), Contour([4, 1, 2, 3, 0]))
    [[0.0, 0.0, 0.0, 0.0, 0.0],
    [1.0, 0.0, 1.0, 1.0, 0.66666666666666663],
    [1.0, 0.0, 0.0, 1.0, 0.33333333333333331],
    [1.0, 0.0, 0.0, 0.0, 0.0],
    [1.0, 0.33333333333333331, 0.33333333333333331, 1.0, 0.0]]
    """

    matrices = [numpy.array(cseg.fuzzy_membership_matrix()) for cseg in csegs]
    return [list(sum(a) / float(len(matrices))) for a in zip(*matrices)]


