#!/usr/bin/env python
# -*- coding: utf-8 -*-

import humdrum as h
import re


def test_parse_accidentals():
    n1 = "#"
    n2 = "b"
    assert h.parse_accidentals(n1) == 1
    assert h.parse_accidentals(n2) == -1
    assert h.parse_accidentals(n1 + n1) == 2
    assert h.parse_accidentals(n2 + n2) == -2


def test_parse_pitch():
    assert h.parse_pitch("**pitch") == "**midi"
    assert h.parse_pitch("4C4") == 60
    assert h.parse_pitch("4Eb4") == 63
    assert h.parse_pitch("16F##4") == 67
    assert h.parse_pitch(".") == '.'
    assert h.parse_pitch("*-") == '*-'
    assert h.parse_pitch("=") == '='
