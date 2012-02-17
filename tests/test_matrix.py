# -*- coding: utf-8 -*-

from contour.matrix import ComparisonMatrix
import contour.matrix as matrix

def test_Com_matrix_cseg():
    cm = ComparisonMatrix([[0, 1, 1, 1], [-1, 0, -1, 1], [-1, 1, 0, 1], [-1, -1, -1, 0]])
    assert cm.cseg() == [0, 2, 1, 3]

def test_Com_matrix_diagonal():
    cm = ComparisonMatrix([[0, 1, 1, 1], [-1, 0, -1, 1], [-1, 1, 0, 1], [-1, -1, -1, 0]])
    assert cm.diagonal() == [1, -1, 1]

def test_Com_matrix_superior_triangle_1():
    cm = ComparisonMatrix([[0, 1, 1, 1], [-1, 0, -1, 1], [-1, 1, 0, 1], [-1, -1, -1, 0]])
    assert cm.superior_triangle() == [[1, 1, 1], [-1, 1], [1]]

def test_Com_matrix_superior_triangle_2():
    cm = ComparisonMatrix([[0, 1, 1, 1], [-1, 0, -1, 1], [-1, 1, 0, 1], [-1, -1, -1, 0]])
    assert cm.superior_triangle(2) == [[1, 1], [1]]


def test_matrix_from_triangle():
    tri = [[1, 1, 1, 1], [1, 1, 1], [-1, -1], [1]]
    assert matrix.matrix_from_triangle(tri) == [[0, 1, 1, 1, 1],
                                                [-1, 0, 1, 1, 1],
                                                [-1, -1, 0, -1, -1],
                                                [-1, -1, 1, 0, 1],
                                                [-1, -1, 1, -1, 0]]


def test_triangle_zero_replace():
    triangle = [[1, 0, 1, 1], [1, 0, 1], [1, 0], [1]]
    assert matrix.triangle_zero_replace(triangle, -1) == [[1, -1, 1, 1], [1, -1, 1],
                                                          [1, -1], [1]]


def test_triangle_zero_replace_to_cseg():
    triangle = [[1, 1, 1, 1], [1, 0, 1], [-1, 0], [1]]
    assert matrix.triangle_zero_replace_to_cseg(triangle) == [[0, 1, 3, 2, 4], [0, 2, 4, 1, 3]]
