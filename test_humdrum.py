#!/usr/bin/env python
# -*- coding: utf-8 -*-

from humdrum import parse_accidentals, parse_pitch, Spine_file
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


def test_extract_spine():
    spine = Spine_file("data/two-voices.krn", "*Ibass")
    assert spine.extract_spine() == "!!!COM: Silva, Marcos di\n" + \
           "!!!OTL: VLCM Test 1\n!! Test for VLCM\n**kern\n*ICvox\n" + \
           "*Ibass\n*k[b-]\n*d:\n*M3/4\n=1\n4D\n4E\n8F\n8F#\n=2\n1G\n" + \
           ".\n.\n==\n*-\n"
