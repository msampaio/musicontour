# -*- coding: utf-8 -*-

import contour.matrix

def test_Com_matrix_inversion():
    cm = contour.matrix.ComparisonMatrix([[0, 1, 2], [0, 1, 1], [-1, 0, -1],
                                           [-1, 1, 0]])
    assert cm.inversion() == [[2, 1, 0], [0, -1, -1], [1, 0, 1], [1, -1, 0]]
