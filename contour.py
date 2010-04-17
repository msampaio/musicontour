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

    def __init__(self, c):
        self.cseg = c


class Contour_subsets():

    def subsets_count(self, n):
        """Counts contour subset classes with n elements."""

        tuples = [tuple(x) for x in self.ss]
        contour_type = sorted(list(set(tuples)))
        counted_contours = [[x, tuples.count(x)] for x in contour_type]
        return sorted(counted_contours, key=lambda x: x[1], reverse=True)

    def normal_form_subsets(self):
        """Outputs normal form of a list of subsets."""

        return [Contour(x).translation() for x in self.ss]

    def prime_form_subsets(self):
        """Outputs normal form of a list of subsets."""

        return [Contour(x).prime_form() for x in self.ss]

    def normal_form_subsets_count(self, n):
        """Counts subset prime forms with n elements."""

        normal_form = self.normal_form_subsets()
        return Contour_subsets(normal_form).subsets_count(n)

    def prime_form_subsets_count(self, n):
        """Counts subset prime forms with n elements."""

        prime_form = self.prime_form_subsets()
        return Contour_subsets(prime_form).subsets_count(n)

    def __init__(self, subsets):
        self.ss = subsets
