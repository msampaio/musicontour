#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess as sp


class Spine():

    def extract_spine(self):
        """Extracts a spine from a kern file."""

        spine = sp.Popen('extractx -i {0} {1}'.format(self.v, self.f),
                             stdout=sp.PIPE, shell=True)
        return spine.stdout.read()

    def humdrum_pitch(self):
        """Outputs **pitch from a kern file."""

        cmd1 = sp.Popen('extractx -i {0} {1}'.format(self.v, self.f),
                        stdout=sp.PIPE, shell=True)
        cmd2 = sp.Popen('pitch', stdin=cmd1.stdout,
                        stdout=sp.PIPE, shell=True)
        return cmd2.stdout.read()

    def __init__(self, file, voice):
        self.f = file
        self.v = voice
