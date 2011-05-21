#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contour
import utils
import diagonal


class ComparisonMatrix(list):
    """Returns an objcect comparison matrix.
    Input is a list of lists, each of them representing a line in
    matrix:

    >>> ComparisonMatrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]])
      | 0 1 1
    ---------
    0 | - 0 -
    1 | - + 0
    """

    def inversion(self):
        """Returns the inversion of a Comparison Matrix:

        >>> ComparisonMatrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]]).inversion()
        [[0, -1, -1], [1, 0, 1], [1, -1, 0]]
        """

        lines = [contour.Contour(self[0]).inversion()]
        [lines.append([(el * -1) for el in item]) for item in self[1:]]
        return ComparisonMatrix(lines)

    def diagonal(self, n=1):
        """Returns internal diagonal INTn of a Comparison Matrix.

        >>> ComparisonMatrix([[0, 1, 1, 1, 1], [-1, 0, -1, 1, -1],
            [-1, 1, 0, 1, 1], [-1, -1, -1, 0, -1],
            [-1, 1, -1, 1, 0]]).diagonal(2)
        < - + >
        """

        if n < len(self):
            numbered_matrix = sorted(enumerate(self))[1:-n]
            r = [el[i - 1 + n] for (i, el) in numbered_matrix]

            return contour.diagonal.InternalDiagonal(r)

    def __repr__(self):

        cseg = self[0]
        hline = "{0}".format("-" * ((len(cseg) * 2) + 3))
        cseg_str = utils.list_to_string(cseg)
        com_matrix = self[1:]
        com_matrix_str = [(str(cseg[i]) + " | " + \
                           utils.replace_list_to_plus_minus(line)) \
                          for (i, line) in enumerate(com_matrix)]
        half_matrix_1 = "  | " + cseg_str + "\n" + hline + "\n"
        half_matrix_2 = "".join([x + "\n" for x in com_matrix_str])
        return half_matrix_1 + half_matrix_2
