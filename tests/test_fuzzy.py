# -*- coding: utf-8 -*-

import contour.fuzzy as fuzzy
import contour.utils as utils
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


def test__average_matrix_1():
    c1 = Contour([3, 0, 1, 2, 1])
    c2 = Contour([4, 0, 1, 3, 2])
    c3 = Contour([4, 1, 2, 3, 0])
    assert fuzzy.average_matrix(c1, c2, c3) == [[0.0, 0.0, 0.0, 0.0, 0.0],
                                                [1.0, 0.0, 1.0, 1.0, 0.66666666666666663],
                                                [1.0, 0.0, 0.0, 1.0, 0.33333333333333331],
                                                [1.0, 0.0, 0.0, 0.0, 0.0],
                                                [1.0, 0.33333333333333331, 0.33333333333333331, 1.0, 0.0]]


def test__average_matrix_2():
    ## Quinn 1997, table 4, second matrix
    m1 = Contour([5, 4, 3, 6, 1, 2, 3, 2, 4, 3, 0])
    m2a = Contour([6, 7, 4, 3, 0, 2, 1, 0, 3, 4, 5])
    m2b = Contour([5, 7, 4, 3, 0, 2, 1, 0, 3, 4, 6])
    m3a = Contour([7, 6, 4, 1, 5, 3, 0, 2, 4, 5, 3])
    m3b = Contour([4, 6, 5, 3, 2, 6, 5, 1, 0, 6, 5])
    m4a = Contour([8, 7, 5, 6, 3, 5, 4, 0, 2, 5, 1])
    m4b = Contour([7, 6, 4, 5, 4, 3, 1, 0, 3, 5, 2])
    m5 = Contour([7, 3, 6, 5, 4, 1, 0, 2, 4, 2, 4])
    m6a = Contour([7, 5, 2, 0, 1, 3, 6, 5, 4, 3, 1])
    m6b = Contour([8, 6, 3, 0, 1, 5, 7, 6, 5, 4, 2])
    m6c = Contour([8, 6, 3, 2, 4, 6, 7, 5, 2, 0, 1])
    m7a = Contour([8, 6, 4, 2, 7, 4, 1, 3, 0, 2, 5])
    m7b = Contour([6, 5, 3, 1, 4, 2, 0, 1, 3, 4, 2])
    m8a = Contour([7, 5, 2, 7, 6, 4, 1, 0, 2, 5, 3])
    m8b = Contour([7, 5, 3, 7, 6, 2, 1, 0, 3, 5, 4])
    m8c = Contour([6, 4, 2, 6, 5, 3, 1, 0, 2, 4, 3])
    csegs = [m1, m2a, m2b, m3a, m3b, m4a, m4b, m5, m6a, m6b, m6c, m7a, m7b, m8a, m8b, m8c]
    ocurrences = [14, 9, 3, 10, 3, 10, 3, 14, 8, 2, 2, 9, 4, 9, 2, 2]
    # weight csegs by ocurrences number
    weight_csegs = utils.flatten([[cseg for i in range(o)] for cseg, o in zip(csegs, ocurrences)])
    weight_average = fuzzy.average_matrix(*weight_csegs)
    # round numbers like table 4
    rounded = [[round(x, 2) for x in row] for row in weight_average]
    assert rounded == [[0.0, 0.14, 0.03, 0.13, 0.0, 0.03, 0.03, 0.0, 0.0, 0.03, 0.06],
                       [0.86, 0.0, 0.13, 0.39, 0.35, 0.0, 0.12, 0.0, 0.13, 0.0, 0.13],
                       [0.97, 0.87, 0.0, 0.38, 0.37, 0.25, 0.12, 0.12, 0.23, 0.41, 0.33],
                       [0.74, 0.61, 0.62, 0.0, 0.34, 0.37, 0.14, 0.3, 0.23, 0.38, 0.46],
                       [1.0, 0.65, 0.61, 0.66, 0.0, 0.49, 0.49, 0.25, 0.35, 0.5, 0.16],
                       [0.97, 0.95, 0.57, 0.63, 0.51, 0.0, 0.25, 0.23, 0.62, 0.67, 0.36],
                       [0.97, 0.88, 0.72, 0.86, 0.51, 0.75, 0.0, 0.36, 0.67, 0.75, 0.63],
                       [1.0, 0.9, 0.88, 0.66, 0.63, 0.63, 0.64, 0.0, 0.77, 0.66, 0.75],
                       [1.0, 0.73, 0.51, 0.63, 0.52, 0.34, 0.33, 0.23, 0.0, 0.62, 0.36],
                       [0.97, 0.85, 0.24, 0.51, 0.37, 0.13, 0.12, 0.2, 0.38, 0.0, 0.36],
                       [0.94, 0.87, 0.64, 0.54, 0.63, 0.49, 0.35, 0.25, 0.51, 0.64, 0.0]]


def test__comparison__matrix_from_csegs():
    c1 = Contour([3, 0, 1, 2, 1])
    c2 = Contour([4, 0, 1, 3, 2])
    c3 = Contour([4, 1, 2, 3, 0])
    fuzzy. comparison_matrix_from_csegs(c1, c2, c3) == [[0.0, -1.0, -1.0, -1.0, -1.0],
                                                        [1.0, 0.0, 1.0, 1.0, 0.3333333333333333],
                                                        [1.0, -1.0, 0.0, 1.0, 0.0],
                                                        [1.0, -1.0, -1.0, 0.0, -1.0],
                                                        [1.0, -0.3333333333333333, 0.0, 1.0, 0.0]]


def test__entry_numbers():
    assert fuzzy.entry_numbers(Contour([2, 0, 3, 1, 4])) == 20


def test__similarity_increment():
    assert fuzzy.similarity_increment(0.8, 0.9, 2) == 0.45


def test__similarity():
    c1 = Contour([4, 1, 2, 3, 0])
    c2 = Contour([4, 0, 1, 3, 2])
    assert fuzzy.similarity(c1, c2) == 0.8000000000000002