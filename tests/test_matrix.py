# -*- coding: utf-8 -*-

import contour.matrix

def test_Com_matrix_inversion():
    cm = contour.matrix.Comparison_matrix([[0, 1, 2], [0, 1, 1], [-1, 0, -1],
                                           [-1, 1, 0]])
    assert cm.inversion() == [[2, 1, 0], [0, -1, -1], [1, 0, 1], [1, -1, 0]]


def test_Com_str_print():
    cm = contour.matrix.Comparison_matrix([[0, 1, 2], [0, 1, 1], [-1, 0, -1],
                                           [-1, 1, 0]])
    assert cm.str_print() == "  | 0 1 2\n---------\n" + \
           "0 | 0 + +\n1 | - 0 -\n2 | - + 0\n"
