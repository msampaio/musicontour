# -*- coding: utf-8 -*-

from ..contour_module.contour import Contour, Contour_subsets, \
     Internal_diagonal, Comparison_matrix, maximum, minimum, \
     ri_identity_test, cseg_similarity, \
     __contour_classes_generator_cardinality, \
     contour_classes_generator, __intern_diagon_sim, \
     remove_duplicate_tuples, double_replace, \
     replace_list_to_plus_minus, list_to_string


def test_contour_classes_generator_cardinality():
    function = __contour_classes_generator_cardinality
    assert function(4) == [(4, 1, (0, 1, 2, 3)),
                           (4, 2, (0, 1, 3, 2)),
                           (4, 3, (0, 2, 1, 3)),
                           (4, 4, (0, 2, 3, 1)),
                           (4, 5, (0, 3, 1, 2)),
                           (4, 6, (0, 3, 2, 1)),
                           (4, 7, (1, 0, 3, 2)),
                           (4, 8, (1, 3, 0, 2))]


def test_contour_classes_generator():
    function = contour_classes_generator
    assert function(4) == [[(2, 1, (0, 1))],
                           [(3, 1, (0, 1, 2)), (3, 2, (0, 2, 1))],
                           [(4, 1, (0, 1, 2, 3)), (4, 2, (0, 1, 3, 2)),
                            (4, 3, (0, 2, 1, 3)), (4, 4, (0, 2, 3, 1)),
                            (4, 5, (0, 3, 1, 2)), (4, 6, (0, 3, 2, 1)),
                            (4, 7, (1, 0, 3, 2)), (4, 8, (1, 3, 0, 2))]]


def test_double_replace():
    assert double_replace("0 1 -1 1 0") == "0 + - + 0"


def test_replace_list_to_plus_minus():
    assert replace_list_to_plus_minus([0, 1, 1, -1, -1]) == "0 + + - -"


def test_list_to_string():
    assert list_to_string([1, 2, 3]) == "1 2 3"


def test_rotation():
    n = Contour([1, 4, 9, 9, 2, 1])
    assert n.rotation() == [4, 9, 9, 2, 1, 1]
    assert n.rotation(1) == [4, 9, 9, 2, 1, 1]
    assert n.rotation(2) == [9, 9, 2, 1, 1, 4]
    assert n.rotation(20) == [9, 9, 2, 1, 1, 4]


def test_retrograde():
    n = Contour([1, 4, 9, 9, 2, 1])
    assert n.retrograde() == [1, 2, 9, 9, 4, 1]


def test_inversion():
    n = Contour([1, 4, 9, 9, 2, 1])
    assert n.inversion() == [8, 5, 0, 0, 7, 8]


def test_translation():
    n = Contour([1, 4, 9, 9, 2, 1])
    assert n.translation() == [0, 2, 3, 3, 1, 0]


def test_prime_form():
    n1 = Contour([1, 4, 9, 2])
    n2 = Contour([5, 7, 9, 1])
    assert n1.prime_form() == [0, 2, 3, 1]
    assert n2.prime_form() == [0, 3, 2, 1]


def test_remove_adjacent():
    n1 = Contour([1, 4, 9, 9, 2, 1])
    n2 = Contour([0, 1, 1, 2, 3])
    n3 = Contour([1, 4, 9, 9, 2, 4])
    assert n1.remove_adjacent() == [1, 4, 9, 2, 1]
    assert n2.remove_adjacent() == [0, 1, 2, 3]
    assert n3.remove_adjacent() == [1, 4, 9, 2, 4]


def test_Contour_subsets():
    n = Contour([2, 8, 12, 9])
    assert n.subsets(2) == [[2, 8], [2, 9], [2, 12], [8, 9], [8, 12], [12, 9]]
    assert n.subsets(3) == [[2, 8, 9], [2, 8, 12], [2, 12, 9], [8, 12, 9]]


def test_Contour_all_subsets():
    n = Contour([2, 8, 12, 9])
    assert n.all_subsets() == [[2, 8], [2, 9], [2, 12], [8, 9], [8, 12],
                               [12, 9], [2, 8, 9], [2, 8, 12], [2, 12, 9],
                               [8, 12, 9], [2, 8, 12, 9]]


def test_Contour_subsets_adj():
    n = Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
    assert n.subsets_adj(4) == [[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                                [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                                [3, 12, 3, 7]]


def test_cps_position():
    n = Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
    assert n.cps_position() == [(2, 0), (8, 1), (12, 2), (9, 3), (5, 4),
                                (7, 5), (3, 6), (12, 7), (3, 8), (7, 9)]


def test_maxima():
    n = Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
    assert n.maxima() == [0, 2, 5, 7, 9]


def test_minima():
    n = Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
    assert n.minima() == [0, 4, 6, 8, 9]


def test_contour_interval():
    n1 = Contour([1, 5])
    n2 = Contour([3, 0])
    assert n1.contour_interval() == 4
    assert n2.contour_interval() == -3


def test_comparison():
    n1 = Contour([1, 4])
    n2 = Contour([5, 0])
    assert n1.comparison() == 1
    assert n2.comparison() == -1


def test_contour_interval_succession():
    n = Contour([0, 1, 3, 2])
    assert n.contour_interval_succession() == [1, 2, -1]


def test_internal_diagonals():
    c1 = Contour([0, 2, 3, 1])
    c2 = Contour([1, 0, 4, 3, 2])
    n1 = 1
    n2 = 2
    assert c1.internal_diagonals(n1) == [1, 1, -1]
    assert c1.internal_diagonals(n2) == [1, -1]
    assert c2.internal_diagonals(n1) == [-1, 1, -1, -1]
    assert c2.internal_diagonals(n2) == [1, 1, -1]


def test_comparison_matrix():
    c1 = Contour([0, 2, 3, 1])
    c2 = Contour([1, 2, 3, 0, 3, 1])
    assert c1.comparison_matrix() == [[0, 2, 3, 1], [0, 1, 1, 1],
                                      [-1, 0, 1, -1], [-1, -1, 0, -1],
                                      [-1, 1, 1, 0]]
    assert c2.comparison_matrix() == [[1, 2, 3, 0, 3, 1], [0, 1, 1, -1, 1, 0],
                                      [-1, 0, 1, -1, 1, -1],
                                      [-1, -1, 0, -1, 0, -1],
                                      [1, 1, 1, 0, 1, 1],
                                      [-1, -1, 0, -1, 0, -1],
                                      [0, 1, 1, -1, 1, 0]]


def test_contour_adjacency_series_vector():
    c1 = Contour([0, 2, 3, 1])
    c2 = Contour([1, 2, 3, 0, 3, 1])
    assert c1.contour_adjacency_series_vector() == [2, 1]
    assert c2.contour_adjacency_series_vector() == [3, 2]


def test_contour_interval_array():
    n = Contour([0, 1, 3, 2])
    assert n.contour_interval_array() == ([2, 2, 1], [1, 0, 0])


def test_contour_class_vector_i():
    n = Contour([0, 1, 3, 2])
    assert n.contour_class_vector_i() == [9, 1]


def test_contour_class_vector_ii():
    n = Contour([0, 1, 3, 2])
    assert n.contour_class_vector_ii() == [5, 1]


def test_contour_segment_class():
    c = Contour([2, 1, 4])
    assert c.contour_segment_class() == (3, 2, (0, 2, 1))


def test_str_print():
    assert Contour([2, 1, 4]).str_print() == "< 2 1 4 >"


def test_subsets_count():
    n = Contour_subsets([[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                         [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                         [3, 12, 3, 7]])
    assert n.subsets_count() == [[(2, 8, 12, 9), 1], [(3, 12, 3, 7), 1],
                                 [(5, 7, 3, 12), 1], [(7, 3, 12, 3), 1],
                                 [(8, 12, 9, 5), 1], [(9, 5, 7, 3), 1],
                                 [(12, 9, 5, 7), 1]]


def test_normal_form_subsets():
    n = Contour_subsets([[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                         [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                         [3, 12, 3, 7]])
    assert n.normal_form_subsets() == [[0, 1, 3, 2], [1, 3, 2, 0],
                                       [3, 2, 0, 1], [3, 1, 2, 0],
                                       [1, 2, 0, 3], [1, 0, 2, 0],
                                       [0, 2, 0, 1]]


def test_prime_form_subsets():
    n = Contour_subsets([[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
                         [9, 5, 7, 3], [5, 7, 3, 12], [7, 3, 12, 3],
                         [3, 12, 3, 7]])
    assert n.prime_form_subsets() == [[0, 1, 3, 2], [0, 2, 3, 1], [0, 1, 3, 2],
                                      [0, 2, 1, 3], [0, 3, 1, 2], [0, 2, 0, 1],
                                      [0, 2, 0, 1]]


def test_normal_form_subsets_count():
    n = Contour_subsets([[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
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
    n = Contour_subsets([[2, 8, 12, 9], [8, 12, 9, 5], [12, 9, 5, 7],
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
    assert ri_identity_test(n1) == 0
    assert ri_identity_test(n2) == 1


def test_maximum():
    n1 = [(5, 0), (8, 1), (4, 2)]
    n2 = [(5, 0), (2, 1), (4, 2)]
    assert maximum(n1) == 1
    assert maximum(n2) == ''


def test_minimum():
    n1 = [(5, 4), (8, 5), (4, 6)]
    n2 = [(5, 2), (0, 3), (4, 4)]
    assert minimum(n1) == ''
    assert minimum(n2) == 3


def test_remove_duplicate_tuples():
    n = [(5, 0), (4, 1), (4, 2), (9, 3), (7, 4), (9, 5), (5, 6)]
    assert remove_duplicate_tuples(n) == [(5, 0), (4, 1), (9, 3),
                                          (7, 4), (9, 5), (5, 6)]


def test___intern_diagon_sim():
    c1 = [0, 2, 3, 1]
    c2 = [3, 1, 0, 2]
    c3 = [2, 0, 1, 3]
    c4 = [1, 3, 2, 0]
    n1 = 1
    n2 = 2
    n3 = 3
    assert __intern_diagon_sim(c1, c2, n1) == 0
    assert __intern_diagon_sim(c1, c2, n2) == 0
    assert __intern_diagon_sim(c1, c2, n3) == 0
    assert __intern_diagon_sim(c1, c3, n1) == 1
    assert __intern_diagon_sim(c1, c3, n2) == 0
    assert __intern_diagon_sim(c1, c3, n3) == 1
    assert __intern_diagon_sim(c1, c4, n1) == 2
    assert __intern_diagon_sim(c1, c4, n2) == 2
    assert __intern_diagon_sim(c1, c4, n3) == 0


def test_cseg_similarity():
    c1 = [0, 2, 3, 1]
    c2 = [3, 1, 0, 2]
    c3 = [1, 0, 4, 3, 2]
    c4 = [3, 0, 4, 2, 1]
    assert cseg_similarity(c1, c2) == 0
    assert cseg_similarity(c3, c4) == 0.8


def test_csegs():
    i1 = Internal_diagonal([-1, 1])
    i2 = Internal_diagonal([-1, 1, 1])
    assert i1.csegs() == [[1, 0, 2], [2, 0, 1]]
    assert i2.csegs() == [[1, 0, 2, 3], [2, 0, 1, 3], [3, 0, 1, 2]]


def test_inversion_Int():
    i1 = Internal_diagonal([-1, 1])
    i2 = Internal_diagonal([-1, 1, 1])
    assert i1.inversion() == [1, -1]
    assert i2.inversion() == [1, -1, -1]


def test_rotation_Int():
    n = Internal_diagonal([1, 1, 0, -1, -1, 1])
    assert n.rotation() == [1, 0, -1, -1, 1, 1]
    assert n.rotation(1) == [1, 0, -1, -1, 1, 1]
    assert n.rotation(2) == [0, -1, -1, 1, 1, 1]
    assert n.rotation(20) == [0, -1, -1, 1, 1, 1]


def test_Int_subsets():
    n = Internal_diagonal([1, 1, 0, -1, -1, 1])
    assert n.subsets(2) == [[-1, -1], [-1, 1], [-1, 1], [0, -1], [0, -1],
                            [0, 1], [1, -1], [1, -1], [1, -1], [1, -1],
                            [1, 0], [1, 0], [1, 1], [1, 1], [1, 1]]
    assert n.subsets(3) == [[-1, -1, 1], [0, -1, -1], [0, -1, 1], [0, -1, 1],
                            [1, -1, -1], [1, -1, -1], [1, -1, 1], [1, -1, 1],
                            [1, -1, 1], [1, -1, 1], [1, 0, -1], [1, 0, -1],
                            [1, 0, -1], [1, 0, -1], [1, 0, 1], [1, 0, 1],
                            [1, 1, -1], [1, 1, -1], [1, 1, 0], [1, 1, 1]]


def test_Int_all_subsets():
    n = Internal_diagonal([1, 1, 0, -1, -1, 1])
    assert n.all_subsets() == [[-1, -1], [-1, 1], [-1, 1], [0, -1], [0, -1],
                               [0, 1], [1, -1], [1, -1], [1, -1], [1, -1],
                               [1, 0], [1, 0], [1, 1], [1, 1], [1, 1],
                               [-1, -1, 1], [0, -1, -1], [0, -1, 1], [0, -1, 1],
                               [1, -1, -1], [1, -1, -1], [1, -1, 1], [1, -1, 1],
                               [1, -1, 1], [1, -1, 1], [1, 0, -1], [1, 0, -1],
                               [1, 0, -1], [1, 0, -1], [1, 0, 1], [1, 0, 1],
                               [1, 1, -1], [1, 1, -1], [1, 1, 0], [1, 1, 1],
                               [0, -1, -1, 1], [1, -1, -1, 1], [1, -1, -1, 1],
                               [1, 0, -1, -1], [1, 0, -1, -1], [1, 0, -1, 1],
                               [1, 0, -1, 1], [1, 0, -1, 1], [1, 0, -1, 1],
                               [1, 1, -1, -1], [1, 1, -1, 1], [1, 1, -1, 1],
                               [1, 1, 0, -1], [1, 1, 0, -1], [1, 1, 0, 1],
                               [1, 0, -1, -1, 1], [1, 0, -1, -1, 1],
                               [1, 1, -1, -1, 1], [1, 1, 0, -1, -1],
                               [1, 1, 0, -1, 1], [1, 1, 0, -1, 1],
                               [1, 1, 0, -1, -1, 1]]


def test_Int_subsets_adj():
    n = Internal_diagonal([1, 1, 0, -1, -1, 1])
    assert n.subsets_adj(2) == [[1, 1], [1, 0], [0, -1], [-1, -1], [-1, 1]]
    assert n.subsets_adj(3) == [[1, 1, 0], [1, 0, -1], [0, -1, -1], [-1, -1, 1]]


def test_Int_str_print():
    i = Internal_diagonal([1, -1, 1])
    assert i.str_print() == "< + - + >"


def test_Com_matrix_inversion():
    cm = Comparison_matrix([[0, 1, 2], [0, 1, 1], [-1, 0, -1], [-1, 1, 0]])
    assert cm.inversion() == [[2, 1, 0], [0, -1, -1], [1, 0, 1], [1, -1, 0]]


def test_Com_str_print():
    cm = Comparison_matrix([[0, 1, 2], [0, 1, 1], [-1, 0, -1], [-1, 1, 0]])
    assert cm.str_print() == "  | 0 1 2\n---------\n" + \
           "0 | 0 + +\n1 | - 0 -\n2 | - + 0\n"
