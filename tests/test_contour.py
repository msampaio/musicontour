# -*- coding: utf-8 -*-

import contour.contour
import py


def test_build_classes():
    function = contour.contour.build_classes
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
    assert contour.contour.subsets_grouped(n, "prime") == \
           'Prime form < 0 1 3 2 > (1)\n< 0 1 4 2 >\n' + \
           'Prime form < 0 2 1 3 > (1)\n< 0 3 1 4 >\n' + \
           'Prime form < 0 2 3 1 > (1)\n< 0 3 4 2 >\n' + \
           'Prime form < 0 3 1 2 > (1)\n< 0 3 1 2 >\n' + \
           'Prime form < 1 3 0 2 > (1)\n< 3 1 4 2 >'


def test_rotation_1():
    n = contour.contour.Contour([1, 4, 9, 9, 2, 1])
    assert n.rotation() == [4, 9, 9, 2, 1, 1]


def test_rotation_2():
    n = contour.contour.Contour([1, 4, 9, 9, 2, 1])
    assert n.rotation(1) == [4, 9, 9, 2, 1, 1]


def test_rotation_3():
    n = contour.contour.Contour([1, 4, 9, 9, 2, 1])
    assert n.rotation(2) == [9, 9, 2, 1, 1, 4]


def test_rotation_4():
    n = contour.contour.Contour([1, 4, 9, 9, 2, 1])
    assert n.rotation(20) == [9, 9, 2, 1, 1, 4]


def test_retrograde():
    n = contour.contour.Contour([1, 4, 9, 9, 2, 1])
    assert n.retrograde() == [1, 2, 9, 9, 4, 1]


def test_inversion():
    n = contour.contour.Contour([1, 4, 9, 9, 2, 1])
    assert n.inversion() == [8, 5, 0, 0, 7, 8]


def test_translation():
    n = contour.contour.Contour([1, 4, 9, 9, 2, 1])
    assert n.translation() == [0, 2, 3, 3, 1, 0]


def test_prime_form_1():
    n = contour.contour.Contour([1, 4, 9, 2])
    assert n.prime_form() == [0, 2, 3, 1]


def test_prime_form_1():
    n = contour.contour.Contour([5, 7, 9, 1])
    assert n.prime_form() == [0, 3, 2, 1]


def test_remove_adjacent_1():
    n = contour.contour.Contour([1, 4, 9, 9, 2, 1])
    assert n.remove_adjacent() == [1, 4, 9, 2, 1]


def test_remove_adjacent_2():
    n = contour.contour.Contour([0, 1, 1, 2, 3])
    assert n.remove_adjacent() == [0, 1, 2, 3]


def test_remove_adjacent_3():
    n = contour.contour.Contour([1, 4, 9, 9, 2, 4])
    assert n.remove_adjacent() == [1, 4, 9, 2, 4]


def test_Contour_subsets_1():
    n = contour.contour.Contour([2, 8, 12, 9])
    assert n.subsets(2) == [[2, 8], [2, 9], [2, 12], [8, 9], [8, 12], [12, 9]]


def test_Contour_subsets_2():
    n = contour.contour.Contour([2, 8, 12, 9])
    assert n.subsets(3) == [[2, 8, 9], [2, 8, 12], [2, 12, 9], [8, 12, 9]]


def test_Contour_subsets_prime():
    n = contour.contour.Contour([0, 3, 1, 4, 2])
    assert n.subsets_prime(4) == {(0, 1, 3, 2): [[0, 1, 4, 2]],
                                  (0, 2, 1, 3): [[0, 3, 1, 4]],
                                  (0, 2, 3, 1): [[0, 3, 4, 2]],
                                  (0, 3, 1, 2): [[0, 3, 1, 2]],
                                  (1, 3, 0, 2): [[3, 1, 4, 2]]}


def test_Contour_subsets_normal():
    n = contour.contour.Contour([0, 3, 1, 4, 2])
    assert n.subsets_normal(4) == {(0, 1, 3, 2): [[0, 1, 4, 2]],
                                   (0, 2, 1, 3): [[0, 3, 1, 4]],
                                   (0, 2, 3, 1): [[0, 3, 4, 2]],
                                   (0, 3, 1, 2): [[0, 3, 1, 2]],
                                   (2, 0, 3, 1): [[3, 1, 4, 2]]}


def test_Contour_all_subsets():
    n = contour.contour.Contour([2, 8, 12, 9])
    assert n.all_subsets() == [[2, 8], [2, 9], [2, 12], [8, 9], [8, 12],
                               [12, 9], [2, 8, 9], [2, 8, 12], [2, 12, 9],
                               [8, 12, 9], [2, 8, 12, 9]]


def test_Contour_all_subsets_prime():
    n = contour.contour.Contour([2, 8, 12])
    assert n.all_subsets_prime() == {(0, 1): [[2, 8], [2, 12], [8, 12]],
                                     (0, 1, 2): [[2, 8, 12]]}


def test_Contour_all_subsets_normal():
    n = contour.contour.Contour([2, 8, 7])
    assert n.all_subsets_normal() == {(0, 1): [[2, 7], [2, 8]],
                                      (0, 2, 1): [[2, 8, 7]],
                                      (1, 0): [[8, 7]]}


def test_Contour_subsets_adj():
    n = contour.contour.Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
    assert n.subsets_adj(4) == [[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                                [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                                [3, 12, 3, 7]]


def test_cps_position():
    n = contour.contour.Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
    assert n.cps_position() == [(2, 0), (8, 1), (12, 2), (9, 3), (5, 4),
                                (7, 5), (3, 6), (12, 7), (3, 8), (7, 9)]


def test_maxima():
    n = [(0, 0), (1, 1), (3, 2), (2, 3), (4, 4)]
    assert contour.contour.maxima(n) == [(0, 0), (3, 2), (4, 4)]


def test_minima():
    n = [(0, 0), (1, 1), (3, 2), (2, 3), (4, 4)]
    assert contour.contour.minima(n) == [(0, 0), (2, 3), (4, 4)]


def test_contour_interval_1():
    n = contour.contour.Contour([1, 5])
    assert n.contour_interval() == 4


def test_contour_interval_2():
    n = contour.contour.Contour([3, 0])
    assert n.contour_interval() == -3


def test_comparison_1():
    n = contour.contour.Contour([1, 4])
    assert n.comparison() == 1


def test_comparison_2():
    n = contour.contour.Contour([5, 0])
    assert n.comparison() == -1


def test_contour_interval_succession():
    n = contour.contour.Contour([0, 1, 3, 2])
    assert n.contour_interval_succession() == [1, 2, -1]


def test_internal_diagonals_1():
    c = contour.contour.Contour([0, 2, 3, 1])
    n = 1
    assert c.internal_diagonals(n) == [1, 1, -1]


def test_internal_diagonals_2():
    c = contour.contour.Contour([0, 2, 3, 1])
    n = 2
    assert c.internal_diagonals(n) == [1, -1]


def test_internal_diagonals_3():
    c = contour.contour.Contour([1, 0, 4, 3, 2])
    n = 1
    assert c.internal_diagonals(n) == [-1, 1, -1, -1]


def test_internal_diagonals_4():
    c = contour.contour.Contour([1, 0, 4, 3, 2])
    n = 2
    assert c.internal_diagonals(n) == [1, 1, -1]


def test_comparison_matrix_1():
    c = contour.contour.Contour([0, 2, 3, 1])
    assert c.comparison_matrix() == [[0, 2, 3, 1], [0, 1, 1, 1],
                                      [-1, 0, 1, -1], [-1, -1, 0, -1],
                                      [-1, 1, 1, 0]]


def test_comparison_matrix_2():
    c = contour.contour.Contour([1, 2, 3, 0, 3, 1])
    assert c.comparison_matrix() == [[1, 2, 3, 0, 3, 1], [0, 1, 1, -1, 1, 0],
                                      [-1, 0, 1, -1, 1, -1],
                                      [-1, -1, 0, -1, 0, -1],
                                      [1, 1, 1, 0, 1, 1],
                                      [-1, -1, 0, -1, 0, -1],
                                      [0, 1, 1, -1, 1, 0]]


def test_contour_adjacency_series_vector_1():
    c = contour.contour.Contour([0, 2, 3, 1])
    assert c.contour_adjacency_series_vector() == [2, 1]


def test_contour_adjacency_series_vector_2():
    c = contour.contour.Contour([1, 2, 3, 0, 3, 1])
    assert c.contour_adjacency_series_vector() == [3, 2]


def test_contour_interval_array():
    n = contour.contour.Contour([0, 1, 3, 2])
    assert n.contour_interval_array() == ([2, 2, 1], [1, 0, 0])


def test_contour_class_vector_i():
    n = contour.contour.Contour([0, 1, 3, 2])
    assert n.contour_class_vector_i() == [9, 1]


def test_contour_class_vector_ii():
    n = contour.contour.Contour([0, 1, 3, 2])
    assert n.contour_class_vector_ii() == [5, 1]


def test_contour_segment_class_1():
    c = contour.contour.Contour([2, 1, 4])
    assert c.contour_segment_class() == (3, 2, (0, 2, 1), False)


def test_contour_segment_class_2():
    c = contour.contour.Contour([3, 1, 0])
    assert c.contour_segment_class() == (3, 1, (0, 1, 2), True)


def test_str_print():
    assert contour.contour.Contour([2, 1, 4]).str_print() == "< 2 1 4 >"


def test_ri_identity_test_1():
    n = contour.contour.Contour([0, 1, 3, 2])
    assert n.ri_identity_test() == False


def test_ri_identity_test():
    n = contour.contour.Contour([1, 0, 3, 2])
    assert n.ri_identity_test() == True
