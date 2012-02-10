# -*- coding: utf-8 -*-

import contour.comparison as comparison
from contour.contour import Contour


def test_cseg_similarity_1():
    c1 = Contour([0, 2, 3, 1])
    c2 = Contour([3, 1, 0, 2])
    assert comparison.cseg_similarity(c1, c2) == 0


def test_cseg_similarity_2():
    c3 = Contour([1, 0, 4, 3, 2])
    c4 = Contour([3, 0, 4, 2, 1])
    assert comparison.cseg_similarity(c3, c4) == 0.8


def test_cseg_similarity_3():
    cseg1 = Contour([0, 1, 2, 3, 4, 5, 6])
    cseg2 = Contour([2, 6, 5, 4, 1, 0, 3])
    assert comparison.cseg_similarity(cseg1, cseg2) == 0.2857142857142857


def test_csegclass_similarity_1():
    cseg1 = Contour([0, 2, 3, 1])
    cseg2 = Contour([3, 1, 0, 2])
    assert comparison.csegclass_similarity(cseg1, cseg2) == 1


def test_csegclass_similarity_2():
    cseg1 = Contour([1, 0, 4, 3, 2])
    cseg2 = Contour([3, 0, 4, 2, 1])
    assert comparison.csegclass_similarity(cseg1, cseg2) == 0.6


def test_cseg_similarity_matrix():
    cseg1 = Contour([1, 0, 4, 3, 2])
    cseg2 = Contour([3, 0, 4, 2, 1])
    fn = comparison.cseg_similarity_matrix([cseg1, cseg2])
    assert fn == [[[1, 0, 4, 3, 2], [3, 0, 4, 2, 1]],
                  [1.0, 0.6],
                  [0.8, 1.0]]


def test_cseg_similarity_matrix_classes():
    fn = comparison.cseg_similarity_matrix_classes(3)
    assert fn == [[[0, 1, 2], [0, 2, 1]], [1.0, 0.66666666666666663],
                  [0.66666666666666663, 1.0]]


def test_subsets_embed_total_number_1():
    c1 = [0, 1, 2, 3]
    c2 = [1, 0, 2]
    assert comparison.subsets_embed_total_number(c1, c2) == 4


def test_subsets_embed_total_number_2():
    c3 = [0, 1, 3, 2]
    c4 = [1, 0, 2]
    assert comparison.subsets_embed_total_number(c3, c4) == 4


def test_subsets_embed_number_1():
    a = [0, 2, 1, 3]
    b = [0, 1, 2]
    assert comparison.subsets_embed_number(a, b) == 2


def test_contour_embed_1():
    a = [0, 2, 1, 3]
    b = [0, 1, 2]
    assert comparison.contour_embed(a, b) == 0.5


def test_contour_similarity_compare_1():
    a = [0, 2, 1, 3]
    b = [0, 1, 2]
    fn = comparison.cseg_similarity_compare(a, b)
    assert fn == ["Cseg embed", 0.5]


def test_contour_similarity_compare_2():
    cseg1 = Contour([0, 2, 1, 3])
    cseg2 = Contour([0, 1, 2, 4])
    fn = comparison.cseg_similarity_compare(cseg1, cseg2)
    assert fn == ["Cseg similarity", 5 / 6.0]


def test___csubseg_mutually_embed_1():
    a = [1, 0, 4, 3, 2]
    b = [2, 0, 1, 4, 3]
    assert comparison.__csubseg_mutually_embed(3, a, b) == [16, 20]


def test___csubseg_mutually_embed_2():
    a = [1, 0, 4, 3, 2]
    b = [2, 0, 1, 4, 3]
    assert comparison.__csubseg_mutually_embed(4, a, b) == [5, 10]


def test_csubseg_mutually_embed_1():
    n = 3
    a = [1, 0, 4, 3, 2]
    b = [2, 0, 1, 4, 3]
    assert comparison.csubseg_mutually_embed(n, a, b) == 0.8


def test_csubseg_mutually_embed_2():
    n = 4
    a = [1, 0, 4, 3, 2]
    b = [2, 0, 1, 4, 3]
    assert comparison.csubseg_mutually_embed(n, a, b) == 0.5


def test__all_contour_mutually_embed():
    cseg1 = Contour([0, 1, 2, 3])
    cseg2 = Contour([0, 1, 2])
    fn = comparison.__all_contour_mutually_embed(cseg1, cseg2)
    assert fn == 0.93333333333333335


def test_all_contour_mutually_embed_1():
    cseg1 = Contour([0, 1, 2, 3])
    cseg2 = Contour([0, 2, 1, 3])
    assert comparison.all_contour_mutually_embed(cseg1, cseg2) == 17.0 / 22


def test_all_contour_mutually_embed_2():
    cseg1 = Contour([0, 1, 2, 3])
    cseg2 = Contour([0, 2, 1, 3, 4])
    assert comparison.all_contour_mutually_embed(cseg1, cseg2) == 29.0 / 37


def test_all_contour_mutually_embed_3():
    cseg1 = Contour([0, 2, 1, 3])
    cseg2 = Contour([0, 2, 1, 3, 4])
    assert comparison.all_contour_mutually_embed(cseg1, cseg2) == 33.0 / 37


def test_operations_comparison():
    cseg1 = Contour([0, 1, 2, 3])
    cseg2 = Contour([3, 1, 2, 0])
    fn = comparison.operations_comparison(cseg1, cseg2)
    assert fn == [[([0, 1, 2, 3], 2, 'internal_diagonals', [1, -1, 1]),
                   ([3, 1, 2, 0], 1, 'internal_diagonals', [1, -1, 1])]]


def test_pretty_operations_comparison():
    cseg1 = Contour([0, 1, 2, 3])
    cseg2 = Contour([3, 1, 2, 0])
    fn = comparison.pretty_operations_comparison(cseg1, cseg2)
    assert fn == '< 0 1 2 3 > [rot1] (internal_diagonals): < + - + >\n' + \
                 '< 3 1 2 0 > [rot1] (internal_diagonals)\n'


def test_cseg_similarity_continuum():
    fn = comparison.cseg_similarity_continuum(Contour([1, 0, 3, 2]))
    assert fn == [[0.5, [[0, 2, 1, 3], [0, 3, 2, 1]]],
                  [0.66666666666666663, [[0, 1, 2, 3], [0, 2, 3, 1],
                                         [0, 3, 1, 2]]],
                  [0.83333333333333337, [[0, 1, 3, 2], [1, 3, 0, 2]]],
                  [1.0, [[1, 0, 3, 2]]]]


def test_cseg_similarity_subsets_continuum():
    fn = comparison.cseg_similarity_subsets_continuum(Contour([0, 1, 2, 3]))
    assert fn == [[[0, 1], 0.58333333333333337],
                  [[0, 1, 2], 0.93333333333333335],
                  [[0, 1, 2, 3], 1.0]]
