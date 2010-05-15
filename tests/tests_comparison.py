# -*- coding: utf-8 -*-

from contour.comparison import (cseg_similarity,
    __intern_diagon_sim,
    print_subsets_grouped,
    subsets_embed_total_number,
    subsets_embed_number, contour_embed, cseg_similarity_compare,
    __csubseg_mutually_embed, csubseg_mutually_embed,
    all_contour_mutually_embed)
import py


def test_subsets_embed_number_1():
    a = [0, 2, 1, 3]
    b = [0, 1, 2]
    assert subsets_embed_number(a, b) == 2


def test_subsets_embed_number_2():
    a = [0, 2, 1, 3]
    b = [0, 1, 2]
    py.test.raises(KeyError, "subsets_embed_number(b, a)")


def test___intern_diagon_sim_1():
    c1 = [0, 2, 3, 1]
    c2 = [3, 1, 0, 2]
    n1 = 1
    assert __intern_diagon_sim(c1, c2, n1) == 0


def test___intern_diagon_sim_2():
    c1 = [0, 2, 3, 1]
    c2 = [3, 1, 0, 2]
    n2 = 2
    assert __intern_diagon_sim(c1, c2, n2) == 0


def test___intern_diagon_sim_3():
    c1 = [0, 2, 3, 1]
    c2 = [3, 1, 0, 2]
    n3 = 3
    assert __intern_diagon_sim(c1, c2, n3) == 0


def test___intern_diagon_sim_4():
    c1 = [0, 2, 3, 1]
    c3 = [2, 0, 1, 3]
    n1 = 1
    assert __intern_diagon_sim(c1, c3, n1) == 1


def test___intern_diagon_sim_5():
    c1 = [0, 2, 3, 1]
    c3 = [2, 0, 1, 3]
    n2 = 2
    assert __intern_diagon_sim(c1, c3, n2) == 0


def test___intern_diagon_sim_6():
    c1 = [0, 2, 3, 1]
    c3 = [2, 0, 1, 3]
    n3 = 3
    assert __intern_diagon_sim(c1, c3, n3) == 1


def test___intern_diagon_sim_7():
    c1 = [0, 2, 3, 1]
    c4 = [1, 3, 2, 0]
    n1 = 1
    assert __intern_diagon_sim(c1, c4, n1) == 2


def test___intern_diagon_sim_8():
    c1 = [0, 2, 3, 1]
    c4 = [1, 3, 2, 0]
    n2 = 2
    assert __intern_diagon_sim(c1, c4, n2) == 2


def test___intern_diagon_sim_9():
    c1 = [0, 2, 3, 1]
    c4 = [1, 3, 2, 0]
    n3 = 3
    assert __intern_diagon_sim(c1, c4, n3) == 0


def test_cseg_similarity_1():
    c1 = [0, 2, 3, 1]
    c2 = [3, 1, 0, 2]
    assert cseg_similarity(c1, c2) == 0


def test_cseg_similarity_2():
    c3 = [1, 0, 4, 3, 2]
    c4 = [3, 0, 4, 2, 1]
    assert cseg_similarity(c3, c4) == 0.8


def test_subsets_embed_total_number_1():
    assert subsets_embed_total_number(3, 2) == 3


def test_subsets_embed_total_number_2():
    assert subsets_embed_total_number(4, 2) == 6


def test_subsets_embed_total_number_3():
    assert subsets_embed_total_number(5, 3) == 10


def test_subsets_embed_total_number_4():
    assert subsets_embed_total_number(3, 3) == 1


def test_subsets_embed_total_number_4():
    assert subsets_embed_total_number(2, 3) == None


def test_contour_embed_1():
    a = [0, 2, 1, 3]
    b = [0, 1, 2]
    assert contour_embed(a, b) == 0.5


def test_contour_similarity_compare_1():
    a = [0, 2, 1, 3]
    b = [0, 1, 2]
    assert cseg_similarity_compare(a, b) == ["Cseg embed", 0.5]


def test_contour_similarity_compare_2():
    a = [0, 2, 1, 3]
    b = [0, 1, 2, 4]
    assert cseg_similarity_compare(a, b) == ["Cseg similarity", 5 / 6.0]


def test___csubseg_mutually_embed_1():
    (a, b) = ([1, 0, 4, 3, 2], [2, 0, 1, 4, 3])
    assert __csubseg_mutually_embed(3, a, b) == [16, 20]


def test___csubseg_mutually_embed_2():
    (a, b) = ([1, 0, 4, 3, 2], [2, 0, 1, 4, 3])
    assert __csubseg_mutually_embed(4, a, b) == [5, 10]


def test_csubseg_mutually_embed_1():
    assert csubseg_mutually_embed(3, [1, 0, 4, 3, 2], [2, 0, 1, 4, 3]) == 0.8


def test_csubseg_mutually_embed_2():
    assert csubseg_mutually_embed(4, [1, 0, 4, 3, 2], [2, 0, 1, 4, 3]) == 0.5


def test_all_csubseg_mutually_embed_1():
    assert all_contour_mutually_embed([0, 1, 2, 3], [0, 2, 1, 3]) == 17.0 / 22


def test_all_csubseg_mutually_embed_2():
    assert all_contour_mutually_embed([0, 1, 2, 3], [0, 2, 1, 3, 4]) == 29.0 / 37


def test_all_csubseg_mutually_embed_3():
    assert all_contour_mutually_embed([0, 2, 1, 3], [0, 2, 1, 3, 4]) == 33.0 / 37
