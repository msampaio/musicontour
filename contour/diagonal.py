#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import itertools
import contour
import utils
import auxiliary

def internal_diagonal_classes(cardinality, prime_algorithm="prime_form_marvin_laprade"):
    """Returns internal diagonal classes of a given cardinality.

    >>> internal_diagonal_classes(4)
    [< + + + >, < + + - >, < + - + >]
    """

    permut = []
    [permut.append([-1, 1]) for n in range(cardinality)]
    permut = sorted(utils.flatten(permut))
    permut = itertools.permutations(permut, cardinality)

    collection = set()

    for el in permut:
        collection.add(tuple(auxiliary.apply_fn(InternalDiagonal(el), prime_algorithm)))

    return sorted([InternalDiagonal(list(x)) for x in list(collection)], reverse=True)


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
        return InternalDiagonal(subset)

    def retrograde(self):
        """Returns internal diagonal retrograde."""

        tmp = self[:]
        tmp.reverse()
        return InternalDiagonal(tmp)

    def inversion(self):
        """Returns Internal diagonal inversion.

        >>> InternalDiagonal([-1, 1, 1]).inversion
        [1, -1, -1]
        """

        return InternalDiagonal([(x * -1) for x in self])

    def subsets(self, n):
        """Returns adjacent and non-adjacent subsets of a given
        contour."""

        int_d = self
        return sorted([InternalDiagonal(list(x)) for x in itertools.combinations(int_d, n)])

    def all_subsets(self):
        """Returns adjacent and non-adjacent subsets of a given
        contour."""

        sizes = range(2, len(self) + 1)
        return utils.flatten([self.subsets(x) for x in sizes])

    def subsets_adj(self, n):
        """Returns adjacent n-elements subsets of a given contour."""

        int_d = self
        return [InternalDiagonal(int_d[i:i + n]) for i in range(len(int_d) - (n - 1))]

    def zero_to_signal(self, signal=1):
        """Substitutes zeros to given signals.

        >>> zero_to_signal(InternalDiagonal([1, -1, 0]), -1)
        < + - - >
        """

        new_diagonal = []

        for el in self:
            if el == 0:
                new_diagonal.append(signal)
            else:
                new_diagonal.append(el)

        return InternalDiagonal(new_diagonal)

    def prime_form(self):
        """Returns internal diagonal prime form.

        The prime form has more pluses than minuses, and is organized
        in a way that most pluses comes first.

        The algorithm:

        1) if there are more minuses than pluses, then invert.

        2) if there are more pluses at the end than the beginning,
        then rotate.
        """

        tmp = self

        if self.count(-1) > self.count(1):
            tmp = self.inversion()

        return sorted([tmp, tmp.retrograde()], reverse=True)[0]

    def __repr__(self):
        return "< {0} >".format(" ".join([utils.double_replace(str(x)) for x in self[:]]))


def csegs_from_diagonals(diagonals_list):
    """Returns possible csegs from a given list of internal diagonals.

    >>> cseg_from_diagonals([InternalDiagonal([1, -1, 1, -1]),
        InternalDiagonal([1, 1, 1]), InternalDiagonal([1, 1]),
        InternalDiagonal([1])])
    < 0 2 1 4 3 >
    """

    coll = []

    for n, diagonal in enumerate(diagonals_list):

        # appends a set with each possible cseg from internal diagonal
        # to coll
        s = set([tuple(x) for x in diagonal.csegs(n + 1)])
        coll.append(s)

    # make the intersection among csegs from internal diagonals
    [coll[0].intersection_update(coll[x]) for x in range(len(coll))]

    return contour.Contour(list(list(coll[0])[0]))
