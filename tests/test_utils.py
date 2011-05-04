# -*- coding: utf-8 -*-

import contour.utils as cu


def test_double_replace():
    assert cu.double_replace("0 1 -1 1 0") == "0 + - + 0"


def test_double_replace():
    assert cu.double_replace("0 1 -1 1 0") == "0 + - + 0"


def test_replace_list_to_plus_minus():
    l = [0, 1, 1, -1, -1]
    assert cu.replace_list_to_plus_minus(l) == "0 + + - -"


def test_list_to_string():
    assert cu.list_to_string([1, 2, 3]) == "1 2 3"


def test_remove_adjacent_1():
    n = [1, 4, 9, 9, 2, 1]
    assert cu.remove_adjacent(n) == [1, 4, 9, 2, 1]


def test_remove_adjacent_2():
    n = [0, 1, 1, 2, 3]
    assert cu.remove_adjacent(n) == [0, 1, 2, 3]


def test_remove_adjacent_3():
    n = [1, 4, 9, 9, 2, 4]
    assert cu.remove_adjacent(n) == [1, 4, 9, 2, 4]


def test_remove_duplicate_tuples():
    n = [(5, 0), (4, 1), (4, 2), (9, 3), (7, 4), (9, 5), (5, 6)]
    assert cu.remove_duplicate_tuples(n) == [(5, 0), (4, 1), (9, 3),
                                             (7, 4), (9, 5), (5, 6)]
