# -*- coding: utf-8 -*-

import contour.fuzzy as fuzzy
from contour.contour import Contour

def test___fuzzy_membership_1():
    assert fuzzy.fuzzy_membership([1, 2]) == 1

def test___fuzzy_membership_2():
    assert fuzzy.fuzzy_membership([2, 1]) == 0

def test___fuzzy_membership_3():
    assert fuzzy.fuzzy_membership([3, 3]) == 0

def test___fuzzy_comparison_1():
    assert fuzzy.fuzzy_comparison([1, 2]) == 1

def test___fuzzy_comparison_2():
    assert fuzzy.fuzzy_comparison([2, 1]) == -1

def test___fuzzy_comparison_3():
    assert fuzzy.fuzzy_comparison([3, 3]) == 0

def test___fuzzy_membership_matrix():
    assert fuzzy.fuzzy_membership_matrix(Contour([0, 2, 1])) == [[0, 1, 1],
                                                                 [0, 0, 0],
                                                                 [0, 1, 0]]

def test___fuzzy_membership_matrix():
    assert fuzzy.fuzzy_comparison_matrix(Contour([0, 2, 1])) == [[0, 1, 1],
                                                                 [-1, 0, -1],
                                                                 [-1, 1, 0]]
