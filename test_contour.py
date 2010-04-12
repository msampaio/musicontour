#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contour as c


def test_contour_class():
    assert c.contour_class([4]) == [0]
    assert c.contour_class([9, 2, 6]) == [2, 0, 1]
    assert c.contour_class([3, 3, 4]) == [0, 0, 1]
    assert c.contour_class([1, 0, 1]) == [1, 0, 1]


def test_absolute_subsets():
    assert c.absolute_subsets([122, 424, 932, 425, 231, 229, 742],
                             3) == [[122, 424, 932], [424, 932, 425],
                                    [932, 425, 231], [425, 231, 229],
                                    [231, 229, 742]]
    assert c.absolute_subsets([122, 424, 932, 425, 231, 229, 742],
                              7) == [[122, 424, 932, 425, 231, 229, 742]]


def test_contour_subsets():
    assert c.contour_subsets([122, 424, 932, 425, 231, 229, 742],
                             3) == [[0, 1, 2], [0, 2, 1], [2, 1, 0],
                                    [2, 1, 0], [1, 0, 2]]
    assert c.contour_subsets([122, 424, 932, 425, 231, 229, 742],
                             7) == [[0, 3, 6, 4, 2, 1, 5]]


def test_contours_count():
    assert c.contours_count([122, 424, 932, 425, 231, 229, 742],
                            3) == [[(2, 1, 0), 2], [(0, 1, 2), 1],
                                   [(0, 2, 1), 1], [(1, 0, 2), 1]]
