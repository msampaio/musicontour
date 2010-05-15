# -*- coding: utf-8 -*-

import contour.utils


def test_double_replace():
    assert contour.utils.double_replace("0 1 -1 1 0") == "0 + - + 0"


def test_replace_list_to_plus_minus():
    l = [0, 1, 1, -1, -1]
    assert contour.utils.replace_list_to_plus_minus(l) == "0 + + - -"


def test_list_to_string():
    assert contour.utils.list_to_string([1, 2, 3]) == "1 2 3"


def test_remove_duplicate_tuples():
    n = [(5, 0), (4, 1), (4, 2), (9, 3), (7, 4), (9, 5), (5, 6)]
    assert contour.utils.remove_duplicate_tuples(n) == [(5, 0), (4, 1), (9, 3),
                                                        (7, 4), (9, 5), (5, 6)]
