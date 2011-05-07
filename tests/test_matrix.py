# -*- coding: utf-8 -*-

from contour.matrix import ComparisonMatrix


def test_Com_matrix_inversion():
    cm = ComparisonMatrix([[0, 1, 2], [0, 1, 1], [-1, 0, -1], [-1, 1, 0]])
    assert cm.inversion() == [[2, 1, 0], [0, -1, -1], [1, 0, 1], [1, -1, 0]]
