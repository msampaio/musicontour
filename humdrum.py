#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess as sp


def kern_file_process(path, basename, voice='*Ibass'):
    """Outputs frequency values."""

    cm1 = sp.Popen('extractx -i {0} {1}'.format(voice,
                                                path + basename + ".krn"),
                           stdout=sp.PIPE, shell=True)
    cm2 = sp.Popen('ditto', stdin=cm1.stdout,
                           stdout=sp.PIPE, shell=True)
    cm3 = sp.Popen('sed \'s/^\[//g\'', stdin=cm2.stdout,
                           stdout=sp.PIPE, shell=True)
    cm4 = sp.Popen('sed \'s/^[0-9].*\]//g\'', stdin=cm3.stdout,
                           stdout=sp.PIPE, shell=True)
    cm5 = sp.Popen('sed \'s/[LJ;_]//g\'', stdin=cm4.stdout,
                           stdout=sp.PIPE, shell=True)
    cm6 = sp.Popen('sed \'s/^[1248]//g\'', stdin=cm5.stdout,
                           stdout=sp.PIPE, shell=True)
    cm7 = sp.Popen('sed \'s/^\.//g\'', stdin=cm6.stdout,
                           stdout=sp.PIPE, shell=True)
    cm8 = sp.Popen('freq', stdin=cm7.stdout,
                           stdout=sp.PIPE, shell=True)
    cm9 = sp.Popen('sed \'s/^\.//g\'', stdin=cm8.stdout,
                           stdout=sp.PIPE, shell=True)
    cm10 = sp.Popen('rid -GLId', stdin=cm9.stdout,
                           stdout=sp.PIPE, shell=True)
    cm11 = sp.Popen('egrep -v \"=|r\"', stdin=cm10.stdout,
                           stdout=sp.PIPE, shell=True)
    cm12 = sp.Popen('uniq', stdin=cm11.stdout,
                           stdout=sp.PIPE, shell=True)
    cm13 = sp.Popen('sed \'/^$/d\'', stdin=cm12.stdout,
                           stdout=sp.PIPE, shell=True)
    cm14 = sp.Popen('sed \'s/X$//g\'', stdin=cm13.stdout,
                           stdout=sp.PIPE, shell=True)
    cmd = cm13
    sp.Popen('mkdir -p /tmp/freq', shell=True)
    with open("/tmp/freq/" + basename + '.freq', "w") as g:
        print(cmd.stdout.read(), file=g)


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
