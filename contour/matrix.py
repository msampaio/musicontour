#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import itertools
import contour
import __utils as utils


# diagonal
def internal_diagonal_classes(cardinality, prime_algorithm="prime_form_marvin_laprade"):
    """Returns internal diagonal classes of a given cardinality.

    >>> internal_diagonal_classes(4)
    [< + + + >, < + + - >, < + - + >]
    """

    permut = []
    [permut.append([-1, 1]) for n in range(cardinality)]
    permut = sorted(utils.flatten(permut))
    permut = itertools.permutations(permut, cardinality)

    # collection
    coll = set()

    for el in permut:
        int_d = utils.apply_fn(InternalDiagonal(el), prime_algorithm)
        coll.add(tuple(int_d))


    return sorted([InternalDiagonal(x) for x in list(coll)], reverse=True)


class InternalDiagonal(list):
    """Returns an objcect Internal diagonal.
    Input is a list of 1 and -1, representing + and - in an internal
    diagonal:

    >>> InternalDiagonal([-1, 1, 1])
    < - + + >
    """

    def __repr__(self):
        data = [utils.double_replace(str(x)) for x in self[:]]
        return "< {0} >".format(" ".join(data))

    def size(self):
        return len(self)

    def csegs(self, d=1):
        """Returns all csegs in normal form that have the given
        internal diagonal. Default diagonal is 1.

        >>> InternalDiagonal([-1, 1, 1]).csegs
        [[1, 0, 2, 3], [2, 0, 1, 3], [3, 0, 1, 2]]
        """

        def __cseg(original, x, d):
            """Returns a list with cseg internal diagonals and cseg
            from a given tuple and diagonal number.
            """

            cseg = contour.Contour(x)
            int_d = cseg.internal_diagonals(d)
            if int_d == original:
                return cseg

        size = len(self) + d
        permut = utils.permut_csegs(size)

        return [__cseg(self, x, d) for x in permut if __cseg(self, x, d)]

    def rotation(self, factor=1):
        """Rotates an internal diagonal around a factor.

        >>> InternalDiagonal([-1, 1, 1, -1]).rotation(2)
        < + - - + >
        """

        return InternalDiagonal(utils.rotation(self, factor))


    def retrogression(self):
        """Returns internal diagonal retrograde.

        >>> InternalDiagonal([1, 1, -1]).retrogression()
        < - + + >
        """

        diagonal = self[:]
        return InternalDiagonal(self.diagonal[::-1])

    def inversion(self):
        """Returns Internal diagonal inversion.

        >>> InternalDiagonal([-1, 1, 1]).inversion()
        < + - - >
        """

        return InternalDiagonal(map(utils.negative, self))

    def subsets(self, n):
        """Returns adjacent and non-adjacent subsets of a given
        contour.

        >>> InternalDiagonal([-1, 1, 1]).subsets(2)
        [< - + >, < - + >, < + + >]
        """

        int_d = self
        comb = itertools.combinations(int_d, n)
        return sorted([InternalDiagonal(x) for x in comb])

    def all_subsets(self):
        """Returns adjacent and non-adjacent subsets of a given
        contour.

        >>> InternalDiagonal([-1, 1, 1]).all_subsets()
        [< - + >, < - + >, < + + >, < - + + >]
        """

        sizes = range(2, len(self) + 1)
        return utils.flatten([self.subsets(x) for x in sizes])

    def subsets_adj(self, n):
        """Returns adjacent n-elements subsets of a given contour.

        >>> InternalDiagonal([-1, 1, 1, 1]).subsets_adj(2)
        [< - + >, < + + >, < + + >]
        """

        int_d = self
        int_range = range(len(int_d) - (n - 1))
        return [InternalDiagonal(int_d[i:i + n]) for i in int_range]

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

        >>> InternalDiagonal([-1, 1, 1, 1]).prime_form()
        < + + + - >
        """

        diagonal = self

        if self.count(-1) > self.count(1):
            diagonal = self.inversion()

        return sorted([diagonal, diagonal.retrogression()], reverse=True)[0]


def csegs_from_diagonals(diagonals_list):
    """Returns possible csegs from a given list of internal diagonals.

    >>> csegs_from_diagonals([InternalDiagonal([1, -1, 1, -1]),
        InternalDiagonal([1, 1, 1]), InternalDiagonal([1, 1]),
        InternalDiagonal([1])])
    < 0 2 1 4 3 >
    """

    coll = []

    try:
        for n, diagonal in enumerate(diagonals_list):

            # appends a set with each possible cseg from internal diagonal
            # to coll
            s = set([tuple(x.cseg) for x in diagonal.csegs(n + 1)])
            coll.append(s)

        # make the intersection among csegs from internal diagonals
        [coll[0].intersection_update(coll[x]) for x in range(len(coll))]

        return contour.Contour(list(coll[0])[0])
    except:
        pass

# crisp
class ComparisonMatrix(list):
    """Returns an objcect comparison matrix.
    Input is a list of lists, each of them representing a line in
    matrix:

    >>> ComparisonMatrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]])
    0 + +
    - 0 -
    - + 0
    """

    def __repr__(self):
        return "\n".join([str(utils.replace_list_to_plus_minus(line)) for line in self])

    def size(self):
        """Returns cseg size."""

        return len(self)

    def cseg(self):
        """Returns a cseg from Matrix.

        >>> ComparisonMatrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]]).cseg()
        < 0 2 1 >
        """

        return contour.Contour([(self.size() - 1 - sum(row)) // 2 for row in self]).translation()

    def diagonal(self, n=1):
        """Returns a diagonal from Matrix. In main diagonal, n = 0.

        >>> ComparisonMatrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]]).diagonal()
        < + - >
        """

        if n < self.size():
            diagonal_size = self.size() - n
            return InternalDiagonal([self[x][x + n] for x in range(diagonal_size)])

    def superior_triangle(self, n=1):
        """Returns the right superior triangle from a matrix. The main
        diagonal is excluded.

        >>> ComparisonMatrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]]).superior_triangle()
        [[1, 1], [-1]]
        """

        if n < self.size():
            return [line[i + n:] for i, line in enumerate(self) if line][:-n]

    def fuzzy_matrix(self):
        """Returns a fuzzy ascent membership matrix from a crisp
        matrix."""

        return FuzzyMatrix([[utils.ascent_membership(column) for column in row] for row in self])


    def show(self):
        """Returns matrix with a matrix with cseg in a visual way.

        >>> ComparisonMatrix([[0, 1, 1, 1], [-1, 0, -1, 1], [-1, 1, 0, 1], [-1, -1, -1, 0]]).display()
        '  | 0 2 1 3\n-----------\n0 | 0 + + +\n2 | - 0 - +\n1 | - + 0 +\n3 | - - - 0'
        """

        def __lines(el, line, cseg):
            return str(cseg[el]) + " | " + str(utils.replace_list_to_plus_minus(line))

        cseg = self.cseg()
        first_line = "  | {0}\n".format(" ".join([str(x) for x in cseg]))
        second_line = "---" + ("-" * self.size() * 2) + "\n"
        other_lines = "\n".join([__lines(el, line, cseg) for el, line in enumerate(self)])
        return first_line + second_line + other_lines


def matrix_from_triangle(triangle):
    """Returns a complete comparison matrix from a given superior
    triangle.

    >>> matrix_from_triangle([[1, 1, 1, 1], [1, 1, 1], [-1, -1], [1]])
    0 + + + +
    - 0 + + +
    - - 0 - -
    - - + 0 +
    - - + - 0
    """

    matrix = []
    for n in range(0, len(triangle) + 1):
        line = []
        for x in range(n):
            line.append(utils.negative(triangle[x][n - x - 1]))
        line.append(0)
        if n < len(triangle):
            line.extend(triangle[n])
        matrix.append(line)
    return ComparisonMatrix(matrix)


def triangle_zero_replace(triangle, replacement):
    """Returns a triangle with zeros replaced by the given replacement factor.

    >>> triangle_zero_replace([[1, 0, 1, 1], [1, 0, 1], [1, 0], [1]], -1)
    [[1, -1, 1, 1], [1, -1, 1], [1, -1], [1]]
    """

    return [contour.utils.replace_all(row, replacement) for row in triangle]


def triangle_zero_replace_to_cseg(triangle):
    """Returns two csegs obtained by zero to 1/-1 replacement.

    >>> triangle_zero_replace_to_cseg([[1, 1, 1, 1], [1, 0, 1], [-1, 0], [1])
    [< 0 1 3 2 4 >, < 0 2 4 1 3 >]
    """

    pair = []
    for r in [1, -1]:
        new_triangle = triangle_zero_replace(triangle, r)
        new_matrix = matrix_from_triangle(new_triangle)
        pair.append(new_matrix.cseg())
    return [contour.Contour(x) for x in pair]


# fuzzy
class FuzzyMatrix(list):
    """Returns an object fuzzy matrix.
    Input is a list of lists, each of them representing a line in
    matrix:

    >>> FuzzyMatrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]])
    """

    def __repr__(self):
        return "\n".join([" ".join([str(row) for row in line]) for line in self])

    def except_zero_diagonal(self):
        """Returns the matrix without main zero diagonal.

        >>> FuzzyMatrix([[0, 1, 1, 1],
                         [0, 0, 1, 1],
                         [0, 0, 0, 0],
                         [0, 0, 1, 0]]).except_zero_diagonal()
        [[1, 1, 1], [0, 1, 1], [0, 0, 0], [0, 0, 1]]
        """

        return [[el for r, el in enumerate(line) if l != r] for l, line in enumerate(self)]

    def comparison(self):
        """Returns a comparison matrix from an average matrix.

        >>> FuzzyMatrix([[0.0, 0.0, 0.0, 0.0, 0.0],
        ...
                         [1.0, 0.33333333333333331, 0.33333333333333331, 1.0, 0.0]]).comparison()
        [[0.0, -1.0, -1.0, -1.0, -1.0],
        ...
        [1.0, -0.3333333333333333, 0.0, 1.0, 0.0]]
        """

        def __comparison(matrix, a, b):
            return matrix.item((x, y)) - matrix.item((y, x))

        def __product(rsize, n):
            return itertools.product(range(n, n + 1), rsize)

        size = len(self)
        rsize = range(size)
        matrix = numpy.matrix(self)

        fm = [[__comparison(matrix, x, y)  for x, y in __product(rsize, n)] for n in rsize]
        return FuzzyMatrix(fm)

def average_matrix(*csegs):
    """Returns the matrix of an average contour from a list of
    contours. Quinn 1997.

    >>> average_matrix(Contour([3, 0, 1, 2, 1]), Contour([4, 0, 1, 3, 2]), Contour([4, 1, 2, 3, 0]))
    [[0.0, 0.0, 0.0, 0.0, 0.0],
    ...
    [1.0, 0.33333333333333331, 0.33333333333333331, 1.0, 0.0]]
    """

    matrices = [numpy.array(cseg.fuzzy_membership_matrix()) for cseg in csegs]
    return [list(sum(a) / float(len(matrices))) for a in zip(*matrices)]
