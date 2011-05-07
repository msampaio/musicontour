# -*- coding: utf-8 -*-

from contour.diagonal import InternalDiagonal


def test_csegs_1():
    i = InternalDiagonal([-1, 1])
    assert i.csegs() == [[1, 0, 2], [2, 0, 1]]


def test_csegs_2():
    i = InternalDiagonal([-1, 1, 1])
    assert i.csegs() == [[1, 0, 2, 3], [2, 0, 1, 3], [3, 0, 1, 2]]


def test_inversion_Int_1():
    i = InternalDiagonal([-1, 1])
    assert i.inversion() == [1, -1]


def test_inversion_Int_2():
    i = InternalDiagonal([-1, 1, 1])
    assert i.inversion() == [1, -1, -1]


def test_rotation_Int_1():
    i = InternalDiagonal([1, 1, 0, -1, -1, 1])
    assert i.rotation() == [1, 0, -1, -1, 1, 1]


def test_rotation_Int_2():
    i = InternalDiagonal([1, 1, 0, -1, -1, 1])
    assert i.rotation(1) == [1, 0, -1, -1, 1, 1]


def test_rotation_Int_3():
    i = InternalDiagonal([1, 1, 0, -1, -1, 1])
    assert i.rotation(2) == [0, -1, -1, 1, 1, 1]


def test_rotation_Int_4():
    i = InternalDiagonal([1, 1, 0, -1, -1, 1])
    assert i.rotation(20) == [0, -1, -1, 1, 1, 1]


def test_Int_subsets_1():
    i = InternalDiagonal([1, 1, 0, -1, -1, 1])
    assert i.subsets(2) == [[-1, -1], [-1, 1], [-1, 1], [0, -1], [0, -1],
                            [0, 1], [1, -1], [1, -1], [1, -1], [1, -1],
                            [1, 0], [1, 0], [1, 1], [1, 1], [1, 1]]


def test_Int_subsets_2():
    i = InternalDiagonal([1, 1, 0, -1, -1, 1])
    assert i.subsets(3) == [[-1, -1, 1], [0, -1, -1], [0, -1, 1], [0, -1, 1],
                            [1, -1, -1], [1, -1, -1], [1, -1, 1], [1, -1, 1],
                            [1, -1, 1], [1, -1, 1], [1, 0, -1], [1, 0, -1],
                            [1, 0, -1], [1, 0, -1], [1, 0, 1], [1, 0, 1],
                            [1, 1, -1], [1, 1, -1], [1, 1, 0], [1, 1, 1]]


def test_Int_all_subsets():
    i = InternalDiagonal([1, 1, 0, -1, -1, 1])
    assert i.all_subsets() == [[-1, -1], [-1, 1], [-1, 1], [0, -1], [0, -1],
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
    i = InternalDiagonal([1, 1, 0, -1, -1, 1])
    assert i.subsets_adj(2) == [[1, 1], [1, 0], [0, -1], [-1, -1], [-1, 1]]


def test_Int_subsets_adj_2():
    i = InternalDiagonal([1, 1, 0, -1, -1, 1])
    assert i.subsets_adj(3) == [[1, 1, 0], [1, 0, -1],
                                [0, -1, -1], [-1, -1, 1]]
