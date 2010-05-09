#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..contour_module.humdrum import (parse_accidentals, parse_pitch,
Spine_file)
import re


def test_parse_accidentals_1():
    assert parse_accidentals("#") == 1


def test_parse_accidentals_2():
    assert parse_accidentals("b") == -1


def test_parse_accidentals_3():
    assert parse_accidentals("##") == 2


def test_parse_accidentals_4():
    assert parse_accidentals("bb") == -2


def test_parse_pitch_1():
    assert parse_pitch("**pitch") == "**midi"


def test_parse_pitch_1():
    assert parse_pitch("4C4") == 60


def test_parse_pitch_1():
    assert parse_pitch("4Eb4") == 63


def test_parse_pitch_1():
    assert parse_pitch("16F##4") == 67


def test_parse_pitch_1():
    assert parse_pitch(".") == '.'


def test_parse_pitch_1():
    assert parse_pitch("*-") == '*-'


def test_parse_pitch_1():
    assert parse_pitch("=") == '='


def test_extract_spine():
    spine = Spine_file("data/two-voices.krn", "*Ibass")
    assert spine.extract_spine() == "!!!COM: Silva, Marcos di\n" + \
           "!!!OTL: VLCM Test 1\n!! Test for VLCM\n**kern\n*ICvox\n" + \
           "*Ibass\n*k[b-]\n*d:\n*M3/4\n=1\n4D\n4E\n8F\n8F#\n=2\n1G\n" + \
           ".\n.\n==\n*-\n"
