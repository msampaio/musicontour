# -*- coding: utf-8 -*-

import contour.contour as cc
import py


def test_build_classes():
    function = cc.build_classes
    assert function(4) == [[(2, 1, (0, 1), True)],
                           [(3, 1, (0, 1, 2), True), (3, 2, (0, 2, 1), False)],
                           [(4, 1, (0, 1, 2, 3), True),
                            (4, 2, (0, 1, 3, 2), False),
                            (4, 3, (0, 2, 1, 3), True),
                            (4, 4, (0, 2, 3, 1), False),
                            (4, 5, (0, 3, 1, 2), False),
                            (4, 6, (0, 3, 2, 1), False),
                            (4, 7, (1, 0, 3, 2), True),
                            (4, 8, (1, 3, 0, 2), True)]]


def test_subsets_grouped():
    n = {(0, 1, 3, 2): [[0, 1, 4, 2]],
         (0, 2, 1, 3): [[0, 3, 1, 4]],
         (0, 2, 3, 1): [[0, 3, 4, 2]],
         (0, 3, 1, 2): [[0, 3, 1, 2]],
         (1, 3, 0, 2): [[3, 1, 4, 2]]}
    assert cc.subsets_grouped(n, "prime") == \
           'Prime form < 0 1 3 2 > (1)\n< 0 1 4 2 >\n' + \
           'Prime form < 0 2 1 3 > (1)\n< 0 3 1 4 >\n' + \
           'Prime form < 0 2 3 1 > (1)\n< 0 3 4 2 >\n' + \
           'Prime form < 0 3 1 2 > (1)\n< 0 3 1 2 >\n' + \
           'Prime form < 1 3 0 2 > (1)\n< 3 1 4 2 >'


def test_rotation_1():
    n = cc.Contour([1, 4, 9, 9, 2, 1])
    assert n.rotation() == [4, 9, 9, 2, 1, 1]


def test_rotation_2():
    n = cc.Contour([1, 4, 9, 9, 2, 1])
    assert n.rotation(1) == [4, 9, 9, 2, 1, 1]


def test_rotation_3():
    n = cc.Contour([1, 4, 9, 9, 2, 1])
    assert n.rotation(2) == [9, 9, 2, 1, 1, 4]


def test_rotation_4():
    n = cc.Contour([1, 4, 9, 9, 2, 1])
    assert n.rotation(20) == [9, 9, 2, 1, 1, 4]


def test_retrograde():
    n = cc.Contour([1, 4, 9, 9, 2, 1])
    assert n.retrograde() == [1, 2, 9, 9, 4, 1]


def test_inversion():
    n = cc.Contour([1, 4, 9, 9, 2, 1])
    assert n.inversion() == [8, 5, 0, 0, 7, 8]


def test_translation():
    n = cc.Contour([1, 4, 9, 9, 2, 1])
    assert n.translation() == [0, 2, 3, 3, 1, 0]


def test_prime_form_marvin_laprade_1():
    n = cc.Contour([1, 4, 9, 2])
    assert n.prime_form_marvin_laprade() == [0, 2, 3, 1]


def test_prime_form_marvin_laprade_1():
    n = cc.Contour([5, 7, 9, 1])
    assert n.prime_form_marvin_laprade() == [0, 3, 2, 1]


def test_subsets_1():
    n = cc.Contour([2, 8, 12, 9])
    assert n.subsets(2) == [[2, 8], [2, 9], [2, 12], [8, 9], [8, 12], [12, 9]]


def test_subsets_2():
    n = cc.Contour([2, 8, 12, 9])
    assert n.subsets(3) == [[2, 8, 9], [2, 8, 12], [2, 12, 9], [8, 12, 9]]


def test_subsets_prime():
    n = cc.Contour([0, 3, 1, 4, 2])
    assert n.subsets_prime(4) == {(0, 1, 3, 2): [[0, 1, 4, 2]],
                                  (0, 2, 1, 3): [[0, 3, 1, 4]],
                                  (0, 2, 3, 1): [[0, 3, 4, 2]],
                                  (0, 3, 1, 2): [[0, 3, 1, 2]],
                                  (1, 3, 0, 2): [[3, 1, 4, 2]]}


def test_subsets_normal():
    n = cc.Contour([0, 3, 1, 4, 2])
    assert n.subsets_normal(4) == {(0, 1, 3, 2): [[0, 1, 4, 2]],
                                   (0, 2, 1, 3): [[0, 3, 1, 4]],
                                   (0, 2, 3, 1): [[0, 3, 4, 2]],
                                   (0, 3, 1, 2): [[0, 3, 1, 2]],
                                   (2, 0, 3, 1): [[3, 1, 4, 2]]}


def test_all_subsets():
    n = cc.Contour([2, 8, 12, 9])
    assert n.all_subsets() == [[2, 8], [2, 9], [2, 12], [8, 9], [8, 12],
                               [12, 9], [2, 8, 9], [2, 8, 12], [2, 12, 9],
                               [8, 12, 9], [2, 8, 12, 9]]


def test_all_subsets_prime():
    n = cc.Contour([2, 8, 12])
    assert n.all_subsets_prime() == {(0, 1): [[2, 8], [2, 12], [8, 12]],
                                     (0, 1, 2): [[2, 8, 12]]}


def test_all_subsets_normal():
    n = cc.Contour([2, 8, 7])
    assert n.all_subsets_normal() == {(0, 1): [[2, 7], [2, 8]],
                                      (0, 2, 1): [[2, 8, 7]],
                                      (1, 0): [[8, 7]]}


def test_subsets_adj():
    n = cc.Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
    assert n.subsets_adj(4) == [[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                                [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                                [3, 12, 3, 7]]


def test_cps_position():
    n = cc.Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
    assert n.cps_position() == [(2, 0), (8, 1), (12, 2), (9, 3), (5, 4),
                                (7, 5), (3, 6), (12, 7), (3, 8), (7, 9)]


def test_reduction_algorithm_1():
    c = cc.Contour([0, 4, 3, 2, 5, 5, 1])
    assert c.reduction_algorithm() == [cc.Contour([0, 2, 1]), 2]


def test_reduction_algorithm_2():
    c = cc.Contour([7, 10, 9, 0, 2, 3, 1, 8, 6, 2, 4, 5])
    assert c.reduction_algorithm() == [cc.Contour([2, 3, 0, 1]), 3]


def test_maxima():
    n = [(0, 0), (1, 1), (3, 2), (2, 3), (4, 4)]
    assert cc.maxima(n) == [(0, 0), (3, 2), (4, 4)]


def test_minima():
    n = [(0, 0), (1, 1), (3, 2), (2, 3), (4, 4)]
    assert cc.minima(n) == [(0, 0), (2, 3), (4, 4)]


def test_interval_1():
    n = cc.Contour([1, 5])
    assert n.interval() == 4


def test_interval_2():
    n = cc.Contour([3, 0])
    assert n.interval() == -3


def test_comparison_1():
    n = cc.Contour([1, 4])
    assert n.comparison() == 1


def test_comparison_2():
    n = cc.Contour([5, 0])
    assert n.comparison() == -1


def test_interval_succession():
    n = cc.Contour([0, 1, 3, 2])
    assert n.interval_succession() == [1, 2, -1]


def test_internal_diagonals_1():
    c = cc.Contour([0, 2, 3, 1])
    n = 1
    assert c.internal_diagonals(n) == [1, 1, -1]


def test_internal_diagonals_2():
    c = cc.Contour([0, 2, 3, 1])
    n = 2
    assert c.internal_diagonals(n) == [1, -1]


def test_internal_diagonals_3():
    c = cc.Contour([1, 0, 4, 3, 2])
    n = 1
    assert c.internal_diagonals(n) == [-1, 1, -1, -1]


def test_internal_diagonals_4():
    c = cc.Contour([1, 0, 4, 3, 2])
    n = 2
    assert c.internal_diagonals(n) == [1, 1, -1]


def test_comparison_matrix_1():
    c = cc.Contour([0, 2, 3, 1])
    assert c.comparison_matrix() == [[0, 2, 3, 1], [0, 1, 1, 1],
                                      [-1, 0, 1, -1], [-1, -1, 0, -1],
                                      [-1, 1, 1, 0]]


def test_comparison_matrix_2():
    c = cc.Contour([1, 2, 3, 0, 3, 1])
    assert c.comparison_matrix() == [[1, 2, 3, 0, 3, 1], [0, 1, 1, -1, 1, 0],
                                      [-1, 0, 1, -1, 1, -1],
                                      [-1, -1, 0, -1, 0, -1],
                                      [1, 1, 1, 0, 1, 1],
                                      [-1, -1, 0, -1, 0, -1],
                                      [0, 1, 1, -1, 1, 0]]


def test_adjacency_series_vector_1():
    c = cc.Contour([0, 2, 3, 1])
    assert c.adjacency_series_vector() == [2, 1]


def test_adjacency_series_vector_2():
    c = cc.Contour([1, 2, 3, 0, 3, 1])
    assert c.adjacency_series_vector() == [3, 2]


def test_interval_array():
    n = cc.Contour([0, 1, 3, 2])
    assert n.interval_array() == ([2, 2, 1], [1, 0, 0])


def test_class_vector_i():
    n = cc.Contour([0, 1, 3, 2])
    assert n.class_vector_i() == [9, 1]


def test_class_vector_ii():
    n = cc.Contour([0, 1, 3, 2])
    assert n.class_vector_ii() == [5, 1]


def test_class_index_i():
    n = cc.Contour([0, 1, 3, 2])
    assert n.class_index_i() == 0.9


def test_class_index_ii():
    n = cc.Contour([0, 1, 3, 2])
    assert n.class_index_ii() == 5.0 / 6


def test_segment_class_1():
    c = cc.Contour([2, 1, 4])
    assert c.segment_class() == (3, 2, cc.Contour([0, 2, 1]), False)


def test_segment_class_2():
    c = cc.Contour([3, 1, 0])
    assert c.segment_class() == (3, 1, cc.Contour([0, 1, 2]), True)


def test_ri_identity_test_1():
    n = cc.Contour([0, 1, 3, 2])
    assert n.ri_identity_test() == False


def test_ri_identity_test():
    n = cc.Contour([1, 0, 3, 2])
    assert n.ri_identity_test() == True


def test_class_representatives():
    n = cc.Contour([0, 1, 3, 2])
    assert n.class_representatives() == [cc.Contour([0, 1, 3, 2]),
                                         cc.Contour([3, 2, 0, 1]),
                                         cc.Contour([2, 3, 1, 0]),
                                         cc.Contour([1, 0, 2, 3])]
