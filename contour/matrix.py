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
    0 + +
    - 0 -
    - + 0
    """

    def diagonal(self, n=1):

        if n < len(self):
            diagonal_size = len(self) - n
            return [self[x][x + n] for x in range(diagonal_size)]

    def superior_triangle(self, n=1):

        if n < len(self):
            return [line[i + n:] for i, line in enumerate(self) if line][:-n]

    def __repr__(self):

        return "\n".join([str(utils.replace_list_to_plus_minus(line)) for line in self])
