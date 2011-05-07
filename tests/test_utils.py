# -*- coding: utf-8 -*-

import contour.utils as cu


def test_flatten():
    assert cu.flatten([[0, 1], [2, 3]]) == [0, 1, 2, 3]


def test_filter_int_1():
    assert cu.filter_int(2) == 2


def test_filter_int_2():
    assert cu.filter_int('a') == ''


def test_filter_int_3():
    assert cu.filter_int(set()) == ''


def test_filter_int_4():
    assert cu.filter_int({}) == ''


def test_filter_int_5():
    assert cu.filter_int([1, 2]) == ''


def test_percent():
    n = [[(1, 0), 10], [(0, 1), 11]]
    assert cu.percent(n) == [[(1, 0), '47.62'], [(0, 1), '52.38']]


def test_item_count():
    n = [[0, 1], [2, 3], [4, 5]]
    assert cu.item_count(n) == [[(0, 1), 1], [(4, 5), 1], [(2, 3), 1]]


def test_double_replace():
    assert cu.double_replace("0 1 -1 1 0") == "0 + - + 0"


def test_replace_list_to_plus_minus():
    n = [0, 1, 1, -1, -1]
    assert cu.replace_list_to_plus_minus(n) == "0 + + - -"


def test_replace_plus_minus_to_list():
    n = "0 + + - -"
    assert cu.replace_plus_minus_to_list(n) == [0, 1, 1, -1, -1]


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


def test_pretty_as_cseg():
    n = [1, 3, 5, 4]
    assert cu.pretty_as_cseg(n) == '< 1 3 5 4 >'


def test_greatest_first():
    n1, n2 = [0, 1], [3, 2, 1]
    assert cu.greatest_first(n1, n2) == [[3, 2, 1], [0, 1]]


def test_permut_list():
    lst = [1, 2, 3]
    assert cu.permut_list(lst) == [[1, 2, 3], [1, 3, 2], [2, 1, 3],
                                   [2, 3, 1], [3, 1, 2], [3, 2, 1]]
