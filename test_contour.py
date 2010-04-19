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
    assert n.contour_subsets(4) == [[2, 8, 12, 9], [8, 12, 9, 5],
                                    [12, 9, 5, 7], [9, 5, 7, 3],
                                    [5, 7, 3, 12], [7, 3, 12, 3],
                                    [3, 12, 3, 7]]


def test_cps_position():
    n = c.Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
    assert n.cps_position() == [(2, 0), (8, 1), (12, 2), (9, 3), (5, 4),
                                (7, 5), (3, 6), (12, 7), (3, 8), (7, 9)]


def test_maxima():
    n = c.Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
    assert n.maxima() == [0, 2, 5, 7, 9]


def test_minima():
    n = c.Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
    assert n.minima() == [0, 4, 6, 8, 9]


def test_contour_interval():
    n1 = c.Contour([1, 5])
    n2 = c.Contour([3, 0])
    assert n1.contour_interval() == 4
    assert n2.contour_interval() == -3


def test_comparison():
    n1 = c.Contour([1, 4])
    n2 = c.Contour([5, 0])
    assert n1.comparison() == 1
    assert n2.comparison() == -1


def test_internal_diagonals():
    c1 = c.Contour([0, 2, 3, 1])
    c2 = c.Contour([1, 0, 4, 3, 2])
    n1 = 1
    n2 = 2
    assert c1.internal_diagonals(n1) == [1, 1, -1]
    assert c1.internal_diagonals(n2) == [1, -1]
    assert c2.internal_diagonals(n1) == [-1, 1, -1, -1]
    assert c2.internal_diagonals(n2) == [1, 1, -1]


def test_comparison_matrix():
    c1 = c.Contour([0, 2, 3, 1])
    c2 = c.Contour([1, 2, 3, 0, 3, 1])
    assert c1.comparison_matrix() == [[0, 1, 1, 1], [-1, 0, 1, -1],
                                      [-1, -1, 0, -1], [-1, 1, 1, 0]]
    assert c2.comparison_matrix() == [[0, 1, 1, -1, 1, 0],
                                      [-1, 0, 1, -1, 1, -1],
                                      [-1, -1, 0, -1, 0, -1],
                                      [1, 1, 1, 0, 1, 1],
                                      [-1, -1, 0, -1, 0, -1],
                                      [0, 1, 1, -1, 1, 0]]


def test_contour_adjacency_series_vector():
    c1 = c.Contour([0, 2, 3, 1])
    c2 = c.Contour([1, 2, 3, 0, 3, 1])
    assert c1.contour_adjacency_series_vector() == [2, 1]
    assert c2.contour_adjacency_series_vector() == [3, 2]


def test_contour_interval_succession():
    n = c.Contour([0, 1, 3, 2])
    assert n.contour_interval_succession() == [1, 2, -1]


def test_contour_interval_array():
    n = c.Contour([0, 1, 3, 2])
    assert n.contour_interval_array() == ([2, 2, 1], [1, 0, 0])


def test_contour_class_vector_i():
    n = c.Contour([0, 1, 3, 2])
    assert n.contour_class_vector_i() == [9, 1]


def test_contour_class_vector_ii():
    n = c.Contour([0, 1, 3, 2])
    assert n.contour_class_vector_ii() == [5, 1]


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
    assert n.normal_form_subsets() == [[0, 1, 3, 2], [1, 3, 2, 0],
                                       [3, 2, 0, 1], [3, 1, 2, 0],
                                       [1, 2, 0, 3], [1, 0, 2, 0],
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
    assert n.normal_form_subsets_count() == [[(0, 1, 3, 2), 1],
                                             [(0, 2, 0, 1), 1],
                                             [(1, 0, 2, 0), 1],
                                             [(1, 2, 0, 3), 1],
                                             [(1, 3, 2, 0), 1],
                                             [(3, 1, 2, 0), 1],
                                             [(3, 2, 0, 1), 1]]


def test_prime_form_subsets_count():
    n = c.Contour_subsets([[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                           [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                           [3, 12, 3, 7]])
    assert n.prime_form_subsets_count() == [[(0, 1, 3, 2), 2],
                                            [(0, 2, 0, 1), 2],
                                            [(0, 2, 1, 3), 1],
                                            [(0, 2, 3, 1), 1],
                                            [(0, 3, 1, 2), 1]]


def test_ri_identity_test():
    n1 = [0, 1, 3, 2]
    n2 = [1, 0, 3, 2]
    assert c.ri_identity_test(n1) == 0
    assert c.ri_identity_test(n2) == 1


def test_maximum():
    n1 = [(5, 0), (8, 1), (4, 2)]
    n2 = [(5, 0), (2, 1), (4, 2)]
    assert c.maximum(n1) == 1
    assert c.maximum(n2) == ''


def test_minimum():
    n1 = [(5, 4), (8, 5), (4, 6)]
    n2 = [(5, 2), (0, 3), (4, 4)]
    assert c.minimum(n1) == ''
    assert c.minimum(n2) == 3


def test_remove_duplicate_tuples():
    n = [(5, 0), (4, 1), (4, 2), (9, 3), (7, 4), (9, 5), (5, 6)]
    assert c.remove_duplicate_tuples(n) == [(5, 0), (4, 1), (9, 3),
                                            (7, 4), (9, 5), (5, 6)]


def test___intern_diagon_sim():
    c1 = [0, 2, 3, 1]
    c2 = [3, 1, 0, 2]
    c3 = [2, 0, 1, 3]
    c4 = [1, 3, 2, 0]
    n1 = 1
    n2 = 2
    n3 = 3
    assert c.__intern_diagon_sim(c1, c2, n1) == 0
    assert c.__intern_diagon_sim(c1, c2, n2) == 0
    assert c.__intern_diagon_sim(c1, c2, n3) == 0
    assert c.__intern_diagon_sim(c1, c3, n1) == 1
    assert c.__intern_diagon_sim(c1, c3, n2) == 0
    assert c.__intern_diagon_sim(c1, c3, n3) == 1
    assert c.__intern_diagon_sim(c1, c4, n1) == 2
    assert c.__intern_diagon_sim(c1, c4, n2) == 2
    assert c.__intern_diagon_sim(c1, c4, n3) == 0


def test_cseg_similarity():
    c1 = [0, 2, 3, 1]
    c2 = [3, 1, 0, 2]
    c3 = [1, 0, 4, 3, 2]
    c4 = [3, 0, 4, 2, 1]
    assert c.cseg_similarity(c1, c2) == 0
    assert c.cseg_similarity(c3, c4) == 0.8


def test_contour_classes_generator_cardinality():
    function = __contour_classes_generator_cardinality
    assert c.function(4) == [((4, 1), (0, 1, 2, 3)),
                             ((4, 2), (0, 1, 3, 2)),
                             ((4, 3), (0, 2, 1, 3)),
                             ((4, 4), (0, 2, 3, 1)),
                             ((4, 5), (0, 3, 1, 2)),
                             ((4, 6), (0, 3, 2, 1)),
                             ((4, 7), (1, 0, 3, 2)),
                             ((4, 8), (1, 3, 0, 2))]


def test_contour_classes_generator():
    function = __contour_classes_generator_cardinality
    assert c.function(4) == [[((2, 1), (0, 1))],
                             [((3, 1), (0, 1, 2)), ((3, 2), (0, 2, 1))],
                             [((4, 1), (0, 1, 2, 3)), ((4, 2), (0, 1, 3, 2)),
                              ((4, 3), (0, 2, 1, 3)), ((4, 4), (0, 2, 3, 1)),
                              ((4, 5), (0, 3, 1, 2)), ((4, 6), (0, 3, 2, 1)),
                              ((4, 7), (1, 0, 3, 2)), ((4, 8), (1, 3, 0, 2))]]
