#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import itertools
import contour
import utils
import auxiliary


class InternalDiagonal(list):
    """Returns an objcect Internal diagonal.
    Input is a list of 1 and -1, representing + and - in an internal
    diagonal:

    >>> InternalDiagonal([-1, 1, 1])
    """

    def csegs(self, diagonal=1):
        """Returns all csegs in normal form that have the given
        internal diagonal.

        >>> InternalDiagonal([-1, 1, 1]).csegs
        [[1, 0, 2, 3], [2, 0, 1, 3], [3, 0, 1, 2]]
        """

        size = len(self) + diagonal
        permut = auxiliary.permut_csegs(size)
        int_d_permut = [[contour.Contour(list(x)).internal_diagonals(diagonal), contour.Contour(list(x))] for x in permut]
        result = []
        [result.append(y[1]) for y in int_d_permut if y[0] == self]
        return result

    def rotation(self, factor=1):
        """Rotates an internal diagonal around a factor.

        factor is optional. Default factor=1.

        'n' is the module of input factor. It's allowed to use factor
        numbers greater than internal diagonal size.
        """

        n = factor % len(self)
        subset = self[n:]
        subset.extend(self[0:n])
        return subset

    def retrograde(self):
        """Returns internal diagonal retrograde."""

        self.reverse()
        return self

    def inversion(self):
        """Returns Internal diagonal inversion.

        >>> InternalDiagonal([-1, 1, 1]).inversion
        [1, -1, -1]
        """

        return [(x * -1) for x in self]

    def subsets(self, n):
        """Returns adjacent and non-adjacent subsets of a given
        contour."""

        int_d = self
        return sorted([list(x) for x in itertools.combinations(int_d, n)])

    def all_subsets(self):
        """Returns adjacent and non-adjacent subsets of a given
        contour."""

        sizes = range(2, len(self) + 1)
        return utils.flatten([self.subsets(x) for x in sizes])

    def subsets_adj(self, n):
        """Returns adjacent n-elements subsets of a given contour."""

        int_d = self
        return [int_d[i:i + n] for i in range(len(int_d) - (n - 1))]

    def str_print(self):
        """Prints internal diagonal like used in Contour theories:
        < + - + >
        """

        return "< " + utils.replace_list_to_plus_minus(self) + " >"

    def __repr__(self):
        return "< {0} >".format(" ".join([utils.double_replace(str(x)) for x in self[:]]))
