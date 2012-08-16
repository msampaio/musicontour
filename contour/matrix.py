#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import itertools
import contour
import __utils as utils
import diagonal


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
            return diagonal.InternalDiagonal([self[x][x + n] for x in range(diagonal_size)])

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
                         [1.0, 0.0, 1.0, 1.0, 0.66666666666666663],
                         [1.0, 0.0, 0.0, 1.0, 0.33333333333333331],
                         [1.0, 0.0, 0.0, 0.0, 0.0],
                         [1.0, 0.33333333333333331, 0.33333333333333331, 1.0, 0.0]]).comparison()
        [[0.0, -1.0, -1.0, -1.0, -1.0],
        [1.0, 0.0, 1.0, 1.0, 0.3333333333333333],
        [1.0, -1.0, 0.0, 1.0, 0.0],
        [1.0, -1.0, -1.0, 0.0, -1.0],
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
    [1.0, 0.0, 1.0, 1.0, 0.66666666666666663],
    [1.0, 0.0, 0.0, 1.0, 0.33333333333333331],
    [1.0, 0.0, 0.0, 0.0, 0.0],
    [1.0, 0.33333333333333331, 0.33333333333333331, 1.0, 0.0]]
    """

    matrices = [numpy.array(cseg.fuzzy_membership_matrix()) for cseg in csegs]
    return [list(sum(a) / float(len(matrices))) for a in zip(*matrices)]
