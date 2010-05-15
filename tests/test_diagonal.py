# -*- coding: utf-8 -*-

from contour.contour import Contour
from contour.diagonal import Internal_diagonal


def test_csegs_1():
    i = Internal_diagonal([-1, 1])
    assert i.csegs() == [[1, 0, 2], [2, 0, 1]]


def test_csegs_2():
    i = Internal_diagonal([-1, 1, 1])
    assert i.csegs() == [[1, 0, 2, 3], [2, 0, 1, 3], [3, 0, 1, 2]]


def test_inversion_Int_1():
    i = Internal_diagonal([-1, 1])
    assert i.inversion() == [1, -1]


def test_inversion_Int_2():
    i = Internal_diagonal([-1, 1, 1])
    assert i.inversion() == [1, -1, -1]


def test_rotation_Int_1():
    n = Internal_diagonal([1, 1, 0, -1, -1, 1])
    assert n.rotation() == [1, 0, -1, -1, 1, 1]


def test_rotation_Int_2():
    n = Internal_diagonal([1, 1, 0, -1, -1, 1])
    assert n.rotation(1) == [1, 0, -1, -1, 1, 1]


def test_rotation_Int_3():
    n = Internal_diagonal([1, 1, 0, -1, -1, 1])
    assert n.rotation(2) == [0, -1, -1, 1, 1, 1]


def test_rotation_Int_4():
    n = Internal_diagonal([1, 1, 0, -1, -1, 1])
    assert n.rotation(20) == [0, -1, -1, 1, 1, 1]


def test_Int_subsets_1():
    n = Internal_diagonal([1, 1, 0, -1, -1, 1])
    assert n.subsets(2) == [[-1, -1], [-1, 1], [-1, 1], [0, -1], [0, -1],
                            [0, 1], [1, -1], [1, -1], [1, -1], [1, -1],
                            [1, 0], [1, 0], [1, 1], [1, 1], [1, 1]]


def test_Int_subsets_2():
    n = Internal_diagonal([1, 1, 0, -1, -1, 1])
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
                               [-1, -1, 1], [0, -1, -1], [0, -1, 1],
                               [0, -1, 1], [1, -1, -1], [1, -1, -1],
                               [1, -1, 1], [1, -1, 1], [1, -1, 1], [1, -1, 1],
                               [1, 0, -1], [1, 0, -1], [1, 0, -1], [1, 0, -1],
                               [1, 0, 1], [1, 0, 1], [1, 1, -1], [1, 1, -1],
                               [1, 1, 0], [1, 1, 1], [0, -1, -1, 1],
                               [1, -1, -1, 1], [1, -1, -1, 1], [1, 0, -1, -1],
                               [1, 0, -1, -1], [1, 0, -1, 1], [1, 0, -1, 1],
                               [1, 0, -1, 1], [1, 0, -1, 1], [1, 1, -1, -1],
                               [1, 1, -1, 1], [1, 1, -1, 1], [1, 1, 0, -1],
                               [1, 1, 0, -1], [1, 1, 0, 1], [1, 0, -1, -1, 1],
                               [1, 0, -1, -1, 1], [1, 1, -1, -1, 1],
                               [1, 1, 0, -1, -1], [1, 1, 0, -1, 1],
                               [1, 1, 0, -1, 1], [1, 1, 0, -1, -1, 1]]


def test_Int_subsets_adj_1():
    n = Internal_diagonal([1, 1, 0, -1, -1, 1])
    assert n.subsets_adj(2) == [[1, 1], [1, 0], [0, -1], [-1, -1], [-1, 1]]


def test_Int_subsets_adj_2():
    n = Internal_diagonal([1, 1, 0, -1, -1, 1])
    assert n.subsets_adj(3) == [[1, 1, 0], [1, 0, -1],
                                [0, -1, -1], [-1, -1, 1]]


def test_Int_str_print():
    i = Internal_diagonal([1, -1, 1])
    assert i.str_print() == "< + - + >"
