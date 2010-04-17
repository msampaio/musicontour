#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess as sp
import itertools
import pitch as p
import itertools as i


class Contour():

    def retrograde(self):
        """Returns contour retrograde."""

        self.cseg.reverse()
        return self.cseg

    def inversion(self):
        """Returns contour inversion."""

        maxim = max(self.cseg)
        minim = min(self.cseg)
        axis = ((maxim - minim) / 2.0 + minim)
        return [int("%d" % ((axis * 2) - x)) for x in self.cseg]

    def translation(self):
        """Returns the normal form of a given contour."""

        sorted_contour = sorted(list(set(self.cseg)))
        return [sorted_contour.index(x) for x in self.cseg]

    def prime_form(self):
        """Returns the prime form of a given contour."""

        length = len(self.cseg)
        self.cseg = self.translation()
        if ((length - 1) - self.cseg[-1]) < self.cseg[0]:
            self.cseg = self.inversion()
        else:
            self.cseg
        if self.cseg[-1] < self.cseg[0]:
            self.cseg = self.retrograde()
        else:
            self.cseg
        return self.cseg

    def remove_adjacent(self):
        """Removes adjacent elements from a list."""

        return [a for a, b in i.izip(self.cseg, self.cseg[1:])
                if a != b] + [self.cseg[-1]]

    def contour_subsets(self, n):
        """Returns adjacent n-elements subsets of a given contour."""

        return [self.cseg[i:i + n] for i in range((len(self.cseg) - (n - 1)))]

    def contours_count(self, n):
        """Counts contour subset classes with n elements."""

        normal_form = self.translation()
        subsets = Contour(normal_form).contour_subsets(n)
        tuples = [tuple(x) for x in subsets]
        contour_type = sorted(list(set(tuples)))
        counted_contours = [[x, tuples.count(x)] for x in contour_type]
        return sorted(counted_contours, key=lambda x: x[1], reverse=True)

    def __init__(self, c):
        self.cseg = c
