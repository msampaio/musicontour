#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import contour
import utils

class Comparison_matrix():
    """Returns an objcect comparison matrix.
    Input is a list of lists, each of them representing a line in
    matrix:

    >>> Comparison_matrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]])
    """

    def inversion(self):
        """Returns the inversion of a Comparison Matrix:

        >>> Comparison_matrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]]).inversion()
        [[0, -1, -1], [1, 0, 1], [1, -1, 0]]
        """

        lines = [contour.Contour(self.comparison_matrix[0]).inversion()]
        [lines.append([(el * -1) for el in item]) for item in self.comparison_matrix[1:]]
        return lines

    def str_print(self):
        """Prints comparison matrix like used in Contour theories:

        . | 0 2 1
        ---------
        0 | 0 + +
        2 | - 0 +
        1 | - + 0

        """

        cseg = self.comparison_matrix[0]
        hline = "{0}".format("-" * ((len(cseg) * 2) + 3))
        cseg_str = utils.list_to_string(cseg)
        com_matrix = self.comparison_matrix[1:]
        com_matrix_str = [(str(cseg[i]) + " | " + \
                           utils.replace_list_to_plus_minus(line)) \
                          for (i, line) in enumerate(com_matrix)]
        half_matrix_1 = "  | " + cseg_str + "\n" + hline + "\n"
        half_matrix_2 = "".join([x + "\n" for x in com_matrix_str])
        return half_matrix_1 + half_matrix_2

    def __init__(self, comparison_matrix):
        self.comparison_matrix = comparison_matrix

