#!/usr/bin/env python
# -*- coding: utf-8 -*-

from humdrum import parse_accidentals, parse_pitch
import re


def test_parse_accidentals():
    n1 = "#"
    n2 = "b"
    assert parse_accidentals(n1) == 1
    assert parse_accidentals(n2) == -1
    assert parse_accidentals(n1 + n1) == 2
    assert parse_accidentals(n2 + n2) == -2


def test_parse_pitch():
    assert parse_pitch("**pitch") == "**midi"
    assert parse_pitch("4C4") == 60
    assert parse_pitch("4Eb4") == 63
    assert parse_pitch("16F##4") == 67
    assert parse_pitch(".") == '.'
    assert parse_pitch("*-") == '*-'
    assert parse_pitch("=") == '='
