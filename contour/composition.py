#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import auxiliary
import sys
sys.path.append("/home/marcos/local/music21")
import music21


notes = "c c# d d# e f f# g g# a a# b".split()


def notes_to_music21(notes_list):
    """Generates Music21 measure object from a given Music21 notation
    list of notes.

    >>> notes_to_music21(['c4', 'g4', 'f#4', 'a4', 'e4'])
    <music21.stream.Measure 0 offset=0.0>
    """

    m = music21.stream.Measure()
    for note in notes_list:
        n = music21.note.Note(note)
        n.duration.type = "quarter"
        m.append(n)
    return m


def pitches_to_notes(pitches, offset = 0):
    """Returns Music21 notation pitches from a given list of numeric
    absolute pitches. Accepts octave (offset) as optional. Default is
    0.

    >>> pitches_to_notes([0, 7, 6, 9, 4], 4)
    ['c4', 'g4', 'f#4', 'a4', 'e4']
    """

    result = []

    for pitch in pitches:
        p_class, octave = auxiliary.octave_calculator(pitch)
        octave = octave + offset
        result.append(notes[p_class] + str(octave))

    return result
