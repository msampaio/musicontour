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
