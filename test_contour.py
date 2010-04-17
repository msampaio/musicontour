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
