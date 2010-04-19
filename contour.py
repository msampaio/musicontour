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
        fn argument.

        'n' stores the number of elements that is evaluated.
        'r' means result.
        """

        n = 3
        cseg_length = len(self.cseg)
        pos = self.cps_position()
        cseg_range = range(cseg_length - (n - 1))

        r = [0]
        [r.append(fn(pos[i:i + n])) for i in cseg_range if fn(pos[i:i + n])]
        r.append(cseg_length - 1)
        return r

    def maxima(self):
        """Returns maxima (Morris, 1993) positions in a cseg."""

        return self.max_min(maximum)

    def minima(self):
        """Returns minima (Morris, 1993) positions in a cseg."""

        return self.max_min(minimum)

    def contour_reduction_algorithm(self):
        """Returns Morris (1993) contour reduction from a cseg."""

        maxim = self.maxima()
        minim = self.minima()
        result = u.flatten([maxim, minim])
        result = Contour(sorted(u.flatten([maxim, minim]))).remove_adjacent()
        return [self.cseg[x] for x in result]

    def comparison(self):
        """Returns Morris (1987) comparison [COM(a, b)] for two
        c-pitches."""

        el1, el2 = self.cseg
        delta = (el2 - el1)

        return 0 if abs(delta) == 0 else (delta) / abs(delta)

    def internal_diagonals(self, n):
        """Returns Morris (1987) int_n."""

        subsets = self.contour_subsets(n + 1)
        return [Contour([x[0], x[-1]]).comparison() for x in subsets]

    def comparison_matrix(self):
        """Returns Morris (1987) a cseg COM-Matrix."""

        size = len(self.cseg)
        m = [[a, b] for a in self.cseg for b in self.cseg]
        n = [m[(i * size):((i + 1) * size)] for i in range(size)]
        return [[Contour(x).comparison() for x in n[r]] for r in range(size)]

    def __init__(self, cseg):
        self.cseg = cseg


class Contour_subsets():

    def subsets_count(self):
        """Counts contour subset classes with n elements."""

        tuples = [tuple(x) for x in self.subsets]
        contour_type = sorted(list(set(tuples)))
        counted_contours = [[x, tuples.count(x)] for x in contour_type]
        return sorted(counted_contours, key=lambda x: x[1], reverse=True)

    def normal_form_subsets(self):
        """Outputs normal form of a list of subsets."""

        return [Contour(x).translation() for x in self.subsets]

    def prime_form_subsets(self):
        """Outputs normal form of a list of subsets."""

        return [Contour(x).prime_form() for x in self.subsets]

    def normal_form_subsets_count(self):
        """Counts subset prime forms with n elements."""

        normal_form = self.normal_form_subsets()
        return Contour_subsets(normal_form).subsets_count()

    def prime_form_subsets_count(self):
        """Counts subset prime forms with n elements."""

        prime_form = self.prime_form_subsets()
        return Contour_subsets(prime_form).subsets_count()

    def __init__(self, subsets):
        self.subsets = subsets


def maximum(dur_list):
    """Returns the maximum (Morris, 1993) position of a three
    c-pitches set. The input data is a list of three tuples. Each
    tuple has the c-pitch and its position. """

    (el1, p1), (el2, p2), (el3, p3) = dur_list
    return p2 if el2 >= el1 and el2 >= el3 else ''


def minimum(dur_list):
    """Returns the minimum (Morris, 1993) position of a three
    c-pitches set. The input data is a list of three tuples. Each
    tuple has the c-pitch and its position. """

    (el1, p1), (el2, p2), (el3, p3) = dur_list
    return p2 if el2 <= el1 and el2 <= el3 else ''


def remove_duplicate_tuples(list_of_tuples):
    """Removes tuples that the first item is repeated in adjacent
    tuples. The removed tuple is the second."""

    prev = None
    tmp = []
    for a, b in list_of_tuples:
        if a != prev:
            tmp.append((a, b))
            prev = a
            return tmp


def __intern_diagon_sim(cseg1, cseg2, n):
    """Returns the number of positions where cseg1 and cseg2 have the
    same value in a n-internal diagonal."""

    c1, c2 = Contour(cseg1), Contour(cseg2)
    d1, d2 = c1.internal_diagonals(n), c2.internal_diagonals(n)
    length = len(d1)
    return sum([(1 if d1[i] == d2[i] else 0) for i in range(length)])


def cseg_similarity(cseg1, cseg2):
    """Returns Marvin and Laprade (1987) Csim(a, b). It's a contour
    similarity function that measures similarity between two csegs of
    the same cardinality. The maximum similarity is 1, and minimum is
    0.

    'd' means the number of internal diagonals.

    'triang_pos' is the number of positions in triangle above the zero
    diagonal.

    'similar pos' is the number of positions where cseg1 and cseg2
    have the same value. This variable is calculated with the private
    method __intern_diagon_sim().
    """

    d = range(len(cseg1))
    d.remove(0)
    triangle_pos = sum(d)
    similar_pos = sum([__intern_diagon_sim(cseg1, cseg2, n) for n in d])
    return similar_pos / float(triangle_pos)
