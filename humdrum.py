#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from subprocess import Popen, PIPE
import re
from utils import filter_int


## regular expression to **pitch notes
notes_regex = re.compile('([0-9.]+)(([a-gA-G][b#]*)|r)([0-9]*)')


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

    >>> spine = '**pitch\n4Eb4\n8F##3\n8C4\n*-'
    >>> [parse_pitch(line) for line in spine.split('\n')]
    ['**pitch', 63,55, 60, '*-']
    """

    notes = "C . D . E F . G . A . B".split()

    if line.startswith("**pitch"):
        return "**midi"
    elif (line.startswith("!") or line.startswith("*") or
          line.startswith("=") or line.startswith(".") or
          line == ''):
        return line
    else:
        dur, note, octv = notes_regex.search(line).group(1, 2, 4)
        acc = note[1:]
        note_name = note[:1]
        accidentals = parse_accidentals(acc) if acc else 0

        if note_name == 'r':
            return 'r'
        else:
            octave = 12 * (int(octv) + 1)
            return notes.index(note_name) + accidentals + octave


class Spine_file():

    def extract_spine(self):
        """Extracts a spine from a kern file."""

        spine = Popen('extractx -i {0} {1}'.format(self.voice, self.file),
                             stdout=PIPE, shell=True)
        return spine.stdout.read()

    def humdrum_pitch(self):
        """Outputs **pitch from a kern file."""

        cmd1 = Popen('extractx -i {0} {1}'.format(self.voice, self.file),
                        stdout=PIPE, shell=True)
        cmd2 = Popen('pitch', stdin=cmd1.stdout,
                        stdout=PIPE, shell=True)
        return cmd2.stdout.read()

    def humdrum_yank_abc(self, option):
        """Outputs **pitch of a given excerpt by yank of a kern file."""

        cmd1 = Popen('extractx -i {0} {1}'.format(self.voice, self.file),
                        stdout=PIPE, shell=True)
        cmd2 = Popen('yank {0}'.format(option), stdin=cmd1.stdout,
                        stdout=PIPE, shell=True)
        Popen('hum2abc > /tmp/vlcm.abc', stdin=cmd2.stdout, stdout=PIPE, shell=True)
        Popen('abcm2ps -O /tmp/vlcm.ps /tmp/vlcm.abc', shell=True)
        Popen('gnome-open /tmp/vlcm.ps', shell=True)

    def humdrum_yank_pitch(self, option):
        """Outputs **pitch of a given excerpt by yank of a kern file."""

        cmd1 = Popen('extractx -i {0} {1}'.format(self.voice, self.file),
                        stdout=PIPE, shell=True)
        cmd2 = Popen('yank {0}'.format(option), stdin=cmd1.stdout,
                        stdout=PIPE, shell=True)
        cmd3 = Popen('pitch', stdin=cmd2.stdout,
                        stdout=PIPE, shell=True)
        return cmd3.stdout.read()

    def parse_extract_to_contour_space(self):
        return [filter_int(parse_pitch(line))
                for line in self.humdrum_pitch().split('\n')
                if filter_int(parse_pitch(line))]

    def parse_yank_to_contour_space(self, option):
        return [filter_int(parse_pitch(line))
                for line in self.humdrum_yank_pitch(option).split('\n')
                if filter_int(parse_pitch(line))]

    def __init__(self, file, voice):
        self.file = file
        self.voice = voice
