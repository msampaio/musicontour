# -*- coding: utf-8 -*-

import contour.comparison as comparison
from contour.contour import Contour


def test___intern_diagon_sim_1():
    c1 = [0, 2, 3, 1]
    c2 = [3, 1, 0, 2]
    n1 = 1
    assert comparison.__intern_diagon_sim(c1, c2, n1) == 0


def test___intern_diagon_sim_2():
    c1 = [0, 2, 3, 1]
    c2 = [3, 1, 0, 2]
    n2 = 2
    assert comparison.__intern_diagon_sim(c1, c2, n2) == 0


def test___intern_diagon_sim_3():
    c1 = [0, 2, 3, 1]
    c2 = [3, 1, 0, 2]
    n3 = 3
    assert comparison.__intern_diagon_sim(c1, c2, n3) == 0


def test___intern_diagon_sim_4():
    c1 = [0, 2, 3, 1]
    c3 = [2, 0, 1, 3]
    n1 = 1
    assert comparison.__intern_diagon_sim(c1, c3, n1) == 1


def test___intern_diagon_sim_5():
    c1 = [0, 2, 3, 1]
    c3 = [2, 0, 1, 3]
    n2 = 2
    assert comparison.__intern_diagon_sim(c1, c3, n2) == 0


def test___intern_diagon_sim_6():
    c1 = [0, 2, 3, 1]
    c3 = [2, 0, 1, 3]
    n3 = 3
    assert comparison.__intern_diagon_sim(c1, c3, n3) == 1


def test___intern_diagon_sim_7():
    c1 = [0, 2, 3, 1]
    c4 = [1, 3, 2, 0]
    n1 = 1
    assert comparison.__intern_diagon_sim(c1, c4, n1) == 2


def test___intern_diagon_sim_8():
    c1 = [0, 2, 3, 1]
    c4 = [1, 3, 2, 0]
    n2 = 2
    assert comparison.__intern_diagon_sim(c1, c4, n2) == 2


def test___intern_diagon_sim_9():
    c1 = [0, 2, 3, 1]
    c4 = [1, 3, 2, 0]
    n3 = 3
    assert comparison.__intern_diagon_sim(c1, c4, n3) == 0


def test_single_cseg_similarity_1():
    c1 = [0, 2, 3, 1]
    c2 = [3, 1, 0, 2]
    assert comparison.single_cseg_similarity(c1, c2) == 0


def test_single_cseg_similarity_2():
    c3 = [1, 0, 4, 3, 2]
    c4 = [3, 0, 4, 2, 1]
    assert comparison.single_cseg_similarity(c3, c4) == 0.8


def test_cseg_similarity_1():
    cseg1 = Contour([0, 2, 3, 1])
    cseg2 = Contour([3, 1, 0, 2])
    assert comparison.cseg_similarity(cseg1, cseg2) == 1


def test_cseg_similarity_2():
    cseg1 = Contour([1, 0, 4, 3, 2])
    cseg2 = Contour([3, 0, 4, 2, 1])
    assert comparison.cseg_similarity(cseg1, cseg2) == 0.6


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


def test_all_csubseg_mutually_embed_1():
    cseg1 = Contour([0, 1, 2, 3])
    cseg2 = Contour([0, 2, 1, 3])
    assert comparison.all_contour_mutually_embed(cseg1, cseg2) == 17.0 / 22


def test_all_csubseg_mutually_embed_2():
    cseg1 = Contour([0, 1, 2, 3])
    cseg2 = Contour([0, 2, 1, 3, 4])
    assert comparison.all_contour_mutually_embed(cseg1, cseg2) == 29.0 / 37


def test_all_csubseg_mutually_embed_3():
    cseg1 = Contour([0, 2, 1, 3])
    cseg2 = Contour([0, 2, 1, 3, 4])
    assert comparison.all_contour_mutually_embed(cseg1, cseg2) == 33.0 / 37
