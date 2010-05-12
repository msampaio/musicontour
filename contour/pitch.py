#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

notes_regex = re.compile('([0-9.]+)([a-gA-G])([b#]+)?([0-9]*)')


def parse_accidentals(acc):
    if acc.startswith("#"):
        return len(acc)
    elif acc.startswith("b"):
        return - len(acc)
    else:
        raise "Accidentals should start with # or b."


def parse_pitch(line):
    """Parse pitch and duration in a **pitch spine and return a
    simplified **midi spine.

    The **midi spine that this function return has only the value for
    pitch and no duration or event information whatsoever.

    >>> spine = '**pitch\nEb4\nF##3\nC4\n*-'
    >>> [parse_pitch(line) for line in spine.split('\n')]
    ['**pitch', 61,53, 60, '*-']
    """

    notes = "C D E F G A B".split()

    if line.startswith("**pitch"):
        return "**midi"
    elif (line.startswith("!") or line.startswith("*") or
          line.startswith("=") or line.startswith(".")):
        return line
    elif line == '':
        return ''
    else:
        dur, note, acc, oct = notes_regex.search(line).group(1, 2, 3, 4)
        accidentals = parse_accidentals(acc) if acc else 0
        return notes.index(note) + accidentals + (12 * (int(oct) + 1))
