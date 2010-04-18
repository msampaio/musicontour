#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import itertools as i
import utils as u


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

    def cps_position(self):
        """Returns a tuple with c-pitch and its position for each
        c-pitch of a cseg done."""

        return [(self.cseg[p], p) for p in range(len(self.cseg))]

    def max_min(self, fn):
        """Returns a list with the position of maximum or minimum
        cpitches of a cseg. Maximum or minimum function is defined in
        fn argument."""

        length = len(self.cseg)
        pos = self.cps_position()

        result = [fn(pos[i:i + 3]) for i in range(length - (3 - 1)) if fn(pos[i:i + 3])]
        result.insert(0, 0)
        result.append(length - 1)
        return result

    def maxima(self):
        """Returns maxima positions in a cseg."""

        self.max_min(maximum)

    def minima(self):
        """Returns minima positions in a list."""

        self.max_min(minimum)

    def contour_reduction_algorithm(self):
        """Returns Morris (1993) contour reduction from a cseg."""

        ma = self.maxima()
        mi = self.minima()
        r = u.flatten([ma, mi])
        r = Contour(sorted(u.flatten([ma, mi]))).remove_adjacent()
        return [self.cseg[x] for x in r]

    def comparison(self):
        """Returns Morris (1987) comparison [COM(a, b)] for two
        c-pitches."""

        el1, el2 = self.cseg
        delta = (el2 - el1)

        # opcao 1
        return 0 if abs(delta) == 0 else (delta) / abs(delta)

        # opcao 2 (remove)
        if abs(delta) == 0:
            return 0
        else:
            return (delta) / abs(delta)

    def internal_diagonals(self, n):
        """Returns Morris (1987) int_n."""

        subsets = self.contour_subsets(n + 1)
        return [Contour([x[0], x[-1]]).comparison() for x in subsets]

    def comparison_matrix(self):
        """Returns Morris (1987) a cseg COM-Matrix."""

        size = len(self.cseg)
        m = [[a, b] for a in self.cseg for b in self.cseg]
        n = [m[(i * size):((i + 1) * size)] for i in range(l)]
        return [[Contour(x).comparison() for x in n[r]] for r in range(l)]

    def __init__(self, c):
        self.cseg = c


class Contour_subsets():

    def subsets_count(self):
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

    def normal_form_subsets_count(self):
        """Counts subset prime forms with n elements."""

        normal_form = self.normal_form_subsets()
        return Contour_subsets(normal_form).subsets_count()

    def prime_form_subsets_count(self):
        """Counts subset prime forms with n elements."""

        prime_form = self.prime_form_subsets()
        return Contour_subsets(prime_form).subsets_count()

    def __init__(self, subsets):
        self.ss = subsets


def maximum(dur_list):
    """Returns the maximum (Morris, 1993) position of a three
    c-pitches set. The input data is a list of three tuples. Each
    tuple has the c-pitch and its position. """

    it = iter(dur_list)
    el1, p1 = it.next()
    el2, p2 = it.next()
    el3, p3 = it.next()
    if el2 >= el1 and el2 >= el3:
        return p2
    else:
        return ''


def minimum(dur_list):
    """Returns the minimum (Morris, 1993) position of a three
    c-pitches set. The input data is a list of three tuples. Each
    tuple has the c-pitch and its position. """

    it = iter(dur_list)
    el1, p1 = it.next()
    el2, p2 = it.next()
    el3, p3 = it.next()
    if el2 <= el1 and el2 <= el3:
        return p2
    else:
        return ''
