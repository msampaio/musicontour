#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contour as c


def test_retrograde():
    n = c.Contour([1, 4, 9, 9, 2, 1])
    assert n.retrograde() == [1, 2, 9, 9, 4, 1]


def test_inversion():
    n = c.Contour([1, 4, 9, 9, 2, 1])
    assert n.inversion() == [9, 6, 1, 1, 8, 9]


def test_translation():
    n = c.Contour([1, 4, 9, 9, 2, 1])
    assert n.translation() == [0, 2, 3, 3, 1, 0]


def test_prime_form():
    n1 = c.Contour([1, 4, 9, 2])
    n2 = c.Contour([5, 7, 9, 1])
    assert n1.prime_form() == [0, 2, 3, 1]
    assert n2.prime_form() == [0, 3, 2, 1]


def test_remove_adjacent():
    n1 = c.Contour([1, 4, 9, 9, 2, 1])
    n2 = c.Contour([0, 1, 1, 2, 3])
    n3 = c.Contour([1, 4, 9, 9, 2, 4])
    assert n1.remove_adjacent() == [1, 4, 9, 2, 1]
    assert n2.remove_adjacent() == [0, 1, 2, 3]
    assert n3.remove_adjacent() == [1, 4, 9, 2, 4]


def test_contour_subsets():
    n = c.Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
    assert n.contour_subsets(4) == [[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                                    [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                                    [3, 12, 3, 7]]


def test_subsets_count():
    n = c.Contour_subsets([[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                           [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                           [3, 12, 3, 7]])
    assert n.subsets_count() == [[(2, 8, 12, 9), 1], [(3, 12, 3, 7), 1],
                                 [(5, 7, 3, 12), 1], [(7, 3, 12, 3), 1],
                                 [(8, 12, 9, 5), 1], [(9, 5, 7, 3), 1],
                                 [(12, 9, 5, 7), 1]]


def test_normal_form_subsets():
    n = c.Contour_subsets([[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                           [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                           [3, 12, 3, 7]])
    assert n.normal_form_subsets() == [[0, 1, 3, 2], [1, 3, 2, 0], [3, 2, 0, 1],
                                       [3, 1, 2, 0], [1, 2, 0, 3], [1, 0, 2, 0],
                                       [0, 2, 0, 1]]


def test_prime_form_subsets():
    n = c.Contour_subsets([[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                           [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                           [3, 12, 3, 7]])
    assert n.prime_form_subsets() == [[0, 1, 3, 2], [0, 2, 3, 1], [0, 1, 3, 2],
                                      [0, 2, 1, 3], [0, 3, 1, 2], [0, 2, 0, 1],
                                      [0, 2, 0, 1]]


def test_normal_form_subsets_count():
    n = c.Contour_subsets([[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                           [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                           [3, 12, 3, 7]])
    assert n.normal_form_subsets_count() == [[(0, 1, 3, 2), 1], [(0, 2, 0, 1), 1],
                                             [(1, 0, 2, 0), 1], [(1, 2, 0, 3), 1],
                                             [(1, 3, 2, 0), 1], [(3, 1, 2, 0), 1],
                                             [(3, 2, 0, 1), 1]]


def test_prime_form_subsets_count():
    n = c.Contour_subsets([[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                           [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                           [3, 12, 3, 7]])
    assert n.prime_form_subsets_count() == [[(0, 1, 3, 2), 2], [(0, 2, 0, 1), 2],
                                            [(0, 2, 1, 3), 1], [(0, 2, 3, 1), 1],
                                            [(0, 3, 1, 2), 1]]
