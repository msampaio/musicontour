# -*- coding: utf-8 -*-

import contour.fuzzy as fuzzy
from contour.contour import Contour

def test__membership_1():
    assert fuzzy.membership([1, 2]) == 1

def test__membership_2():
    assert fuzzy.membership([2, 1]) == 0

def test__membership_3():
    assert fuzzy.membership([3, 3]) == 0

def test__comparison_1():
    assert fuzzy.comparison([1, 2]) == 1

def test__comparison_2():
    assert fuzzy.comparison([2, 1]) == -1

def test__comparison_3():
    assert fuzzy.comparison([3, 3]) == 0

def test__FuzzyMatrix_diagonal():
    assert fuzzy.FuzzyMatrix([[0, 1, 1], [-1, 0, -1], [-1, 1, 0]]).diagonal() == [1, -1]

def test__FuzzyMatrix_superior_triangle():
    f = [[0, 1, 1], [-1, 0, -1], [-1, 1, 0]]
    assert fuzzy.FuzzyMatrix(f).superior_triangle() == [[1, 1], [-1]]

def test__FuzzyMatrix_except_zero_diagonal():
    f = [[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 0], [0, 0, 1, 0]]
    assert fuzzy.FuzzyMatrix(f).except_zero_diagonal() == [[1, 1, 1], [0, 1, 1],
                                                           [0, 0, 0], [0, 0, 1]]

def test__comparison():
    f = [[0.0, 0.0, 0.0, 0.0, 0.0],
         [1.0, 0.0, 1.0, 1.0, 0.66666666666666663],
         [1.0, 0.0, 0.0, 1.0, 0.33333333333333331],
         [1.0, 0.0, 0.0, 0.0, 0.0],
         [1.0, 0.33333333333333331, 0.33333333333333331, 1.0, 0.0]]
    assert fuzzy.FuzzyMatrix(f).comparison() == [[0.0, -1.0, -1.0, -1.0, -1.0],
                                                 [1.0, 0.0, 1.0, 1.0, 0.3333333333333333],
                                                 [1.0, -1.0, 0.0, 1.0, 0.0],
                                                 [1.0, -1.0, -1.0, 0.0, -1.0],
                                                 [1.0, -0.3333333333333333, 0.0, 1.0, 0.0]]


def test__membership_similarity_1():
    c1 = Contour([4, 0, 1, 3, 2])
    c2 = Contour([4, 1, 2, 3, 0])
    assert fuzzy.membership_similarity(c1, c2) == 0.8


def test__average_matrix():
    c1 = Contour([3, 0, 1, 2, 1])
    c2 = Contour([4, 0, 1, 3, 2])
    c3 = Contour([4, 1, 2, 3, 0])
    assert fuzzy.average_matrix(c1, c2, c3) == [[0.0, 0.0, 0.0, 0.0, 0.0],
                                                [1.0, 0.0, 1.0, 1.0, 0.66666666666666663],
                                                [1.0, 0.0, 0.0, 1.0, 0.33333333333333331],
                                                [1.0, 0.0, 0.0, 0.0, 0.0],
                                                [1.0, 0.33333333333333331, 0.33333333333333331, 1.0, 0.0]]


def test__comparison__matrix_from_csegs():
    c1 = Contour([3, 0, 1, 2, 1])
    c2 = Contour([4, 0, 1, 3, 2])
    c3 = Contour([4, 1, 2, 3, 0])
    fuzzy. comparison_matrix_from_csegs(c1, c2, c3) == [[0.0, -1.0, -1.0, -1.0, -1.0],
                                                        [1.0, 0.0, 1.0, 1.0, 0.3333333333333333],
                                                        [1.0, -1.0, 0.0, 1.0, 0.0],
                                                        [1.0, -1.0, -1.0, 0.0, -1.0],
                                                        [1.0, -0.3333333333333333, 0.0, 1.0, 0.0]]
