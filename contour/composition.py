#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import auxiliary as aux
import sys
sys.path.append("/home/marcos/local/music21")
import music21
import utils

notes = "c c# d d# e f f# g g# a a# b".split()


def notes_to_music21(notes_list, notes_measure=0):
    """Generates Music21 Part object from a given Music21 notation
    list of notes. The number of notes in each measure is optional. If
    the notes_list is lower than 9, all notes are output in one bar,
    if higher or equal to 9, notes are grouped by 4, unless
    notes_measures is not 0.

    >>> notes_to_music21(['c4', 'g4', 'f#4', 'a4', 'e4'])
    <music21.stream.Part 0 offset=0.0>
    """

    def insert_notes(part, notes_measure):
        """Inserts notes in a Music21 Part object."""

        m = music21.stream.Measure()
        for note in notes_list:
            n = music21.note.Note(note)
            n.duration.type = "quarter"
            m.append(n)
        part.append(m)

    part = music21.stream.Part()
    notes_list_size = len(notes_list)

    if notes_list_size < 9 and notes_measure == 0:
        insert_notes(part, notes_list_size)
    else:
        if notes_measure == 0:
            notes_measure = 4

        sequence = range(0, notes_list_size, notes_measure)
        measures = [notes_list[x:(x + notes_measure)] for x in sequence]

        for measure in measures:
            insert_notes(part, notes_list_size)

    return part


def pitches_to_notes(pitches, offset=0):
    """Returns Music21 notation pitches from a given list of numeric
    absolute pitches. Accepts octave (offset) as optional. Default is
    0.

    >>> pitches_to_notes([0, 7, 6, 9, 4], 4)
    ['c4', 'g4', 'f#4', 'a4', 'e4']
    """

    result = []

    for pitch in pitches:
        p_class, octave = aux.octave_calculator(pitch)
        octave = octave + offset
        result.append(notes[p_class] + str(octave))

    return result


def cseg_pitch_sets_to_music21(cseg, pitch_set, octave=4):
    """Returns a music21.stream.Part object with a musical excerpt with all
    permutations of a given pitch set organized by a given contour on
    a given octave.

    >>> cseg_pitch_sets_to_music21(Contour([0, 1, 2]), [3, 4, 5], 4)
    """

    pitch_numbers = aux.absolute_pitches_permutation(cseg, pitch_set)
    pitch_numbers = utils.flatten(pitch_numbers)
    notes = pitches_to_notes(pitch_numbers, octave)

    return notes_to_music21(notes)
