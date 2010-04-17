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
    notes_regex = re.compile('([0-9.]+)([a-gA-G])([b#]+)?([0-9]*)')
    l1 = "**pitch"
    l2 = "4Eb4"
    l3 = "16F##4"
    l4 = "."
    l5 = "*-"
    l6 = "="
    assert h.parse_pitch(l1) == "**midi"
    assert h.parse_pitch(l2) == 61
    assert h.parse_pitch(l3) == 65
    assert h.parse_pitch(l4) == '.'
    assert h.parse_pitch(l5) == '*-'
    assert h.parse_pitch(l6) == '='
