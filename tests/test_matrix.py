# -*- coding: utf-8 -*-

from contour.matrix import ComparisonMatrix

def test_Com_matrix_diagonal():
    cm = ComparisonMatrix([[0, 1, 1, 1], [-1, 0, -1, 1], [-1, 1, 0, 1], [-1, -1, -1, 0]])
    assert cm.diagonal() == [1, -1, 1]

def test_Com_matrix_superior_triangle_1():
    cm = ComparisonMatrix([[0, 1, 1, 1], [-1, 0, -1, 1], [-1, 1, 0, 1], [-1, -1, -1, 0]])
    assert cm.superior_triangle() == [[1, 1, 1], [-1, 1], [1]]

def test_Com_matrix_superior_triangle_2():
    cm = ComparisonMatrix([[0, 1, 1, 1], [-1, 0, -1, 1], [-1, 1, 0, 1], [-1, -1, -1, 0]])
    assert cm.superior_triangle(2) == [[1, 1], [1]]
