# -*- coding: utf-8 -*-

import contour.auxiliary as auxiliary
from contour.contour import Contour


def test_permut_csegs():
    cardinality = 3
    fn = auxiliary.permut_csegs(cardinality)
    assert fn == [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0],
                    [2, 0, 1], [2, 1, 0]]


def test_apply_fn():
    assert auxiliary.apply_fn(Contour([0, 1, 2]), 'retrograde') == [2, 1, 0]


def test_absolute_pitches():
    cseg = Contour([1, 4, 2, 3, 0])
    pitches_set = [0, 7, 6, 9, 4]
    assert auxiliary.absolute_pitches(cseg, pitches_set) == [12, 31, 18, 21, 4]


def test_absolute_pitches_permutation():
    cseg = Contour([0, 1, 2])
    pitch_set = [3, 4, 5]
    fn = auxiliary.absolute_pitches_permutation(cseg, pitch_set)
    assert fn == [[3, 4, 5], [3, 5, 16], [4, 15, 17], [4, 5, 15],
                  [5, 15, 16], [5, 16, 27]]


def test_octave_calculator():
    assert auxiliary.octave_calculator(50) == (2, 4)


def test_cseg_string_to_Contour():
    assert auxiliary.cseg_string_to_Contour('< 0 1 2 >') == [0, 1, 2]
