#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import itertools as i
import utils as u


def __contour_classes_generator_cardinality(cardinality):
    """Generates contour classes like Marvin and Laprade (1987)
    software for one cardinality

    Returns ((cardinality, number), contour class).

    'base' stores the c-pitches of a given cardinality.

    'permut' stores all permutations with csegs of a given
    cardinality.

    '__cc_repeat stores prime forms of permut. It may have
    duplicates.

    '_cc_no_repeat' stores enumerated sorted contour class without
    duplicates.
    """

    base = range(cardinality)
    permut = i.permutations(base, cardinality)
    __cc_repeat = [tuple(Contour(x).prime_form()) for x in permut]
    __cc_no_repeat = enumerate(sorted(list(set(__cc_repeat))))
    contour_classes = [((cardinality, n + 1), x) for n, x in __cc_no_repeat]
    return contour_classes


def contour_classes_generator(cardinality):
    """Generates contour classes like Marvin and Laprade (1987)
    software."""

    card_list = range(2, (cardinality + 1))
    return [__contour_classes_generator_cardinality(c) for c in card_list]


def print_contour_classes(cardinality):
    """Prints contour classes like Marvin and Laprade (1987).

    'cc' stores flatten contour classes of all cardinalities until the
    one given.
    """

    cc = u.flatten(contour_classes_generator(cardinality))
    new_cc = [(a, b, c) for ((a, b), c) in cc]
    card = 0

    print("C-space segment-classes [by Marvin and Laprade (1987)]\
    \n------------------------------------------------------\n\n")
    for a, b, c in new_cc:
        if a != card:
            print("\nC-space segment classes for cseg cardinality {0}\n\
            \n   Csegclass/Rinv".format(a))
            card = a
        print("   {0}-{1}: {2}".format(a, b, c))


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
        """Returns the normal form (Marvin 1987) of a given contour.
        It's the same of Friedmann (1985, 1987) contour class (CC)."""

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

    def contour_reduction_algorithm_steps(self):
        """Returns a step from Morris (1993) contour reduction."""

        maxim1 = self.maxima()
        minim1 = self.minima()
        step4 = u.flatten([maxim1, minim1])
        step4 = Contour(sorted(u.flatten([maxim1, minim1]))).remove_adjacent()
        result = [self.cseg[x] for x in step4]
        return result

    def contour_reduction_algorithm(self, n):
        """Returns Morris (1993) contour reduction from a cseg n
        times."""

        for i in xrange(n):
            self = Contour(self.contour_reduction_algorithm_steps())
        return self.cseg

    def contour_interval(self):
        """Returns Friedmann (1985) CI, the distance between one
        element in a CC (normal_form cseg here), and a later element
        as signified by +, - and a number (without + here). For
        example, in cseg = [0, 2, 1], CI(0, 2) = 2, e CI(2, 1) = -1."""

        el1, el2 = self.cseg
        return el2 - el1

    def comparison(self):
        """Returns Morris (1987) comparison [COM(a, b)] for two
        c-pitches.

        This method calls contour_interval(), but in contour theory
        there is no relation between them. This calling reason is only
        to reduce code."""

        delta = self.contour_interval()
        return 0 if abs(delta) == 0 else (delta) / abs(delta)

    def contour_interval_succession(self):
        """Return Friedmann (1985) CIS, a series which indicates the
        order of Contour Intervals in a given CC (normal form cseg
        here)."""

        subsets = self.contour_subsets(2)
        return [Contour([x[0], x[-1]]).contour_interval() for x in subsets]

    def internal_diagonals(self, n):
        """Returns Morris (1987) int_n. The first internal diagonal
        (int_1) is the same of Friedmann (1985, 1987) contour
        adjacency series (CC)."""

        subsets = self.contour_subsets(n + 1)
        return [Contour([x[0], x[-1]]).comparison() for x in subsets]

    def comparison_matrix(self):
        """Returns Morris (1987) a cseg COM-Matrix."""

        size = len(self.cseg)
        m = [[a, b] for a in self.cseg for b in self.cseg]
        n = [m[(i * size):((i + 1) * size)] for i in range(size)]
        return [[Contour(x).comparison() for x in n[r]] for r in range(size)]

    def contour_adjacency_series_vector(self):
        """Returns Friedmann (1985) CASV, a two digit summation of ups
        and downs of a CAS (internal diagonal n=1 here). For example,
        [2, 1] means 2 ups and 1 down.

        'internal_diagonal' stores cseg internal diagonal, n = 1.

        'ups' stores the total number of ups

        'downs' stores the total number of downs
        """

        internal_diagonal = self.internal_diagonals(1)
        ups = sum([(x if x > 0 else 0) for x in internal_diagonal])
        downs = sum([(x if x < 0 else 0) for x in internal_diagonal])
        return [ups, abs(downs)]

    def contour_interval_array(self):
        """Return Friedmann (1985) CIA, an ordered series of numbers
        that indicates the multiplicity of each Contour Interval type
        in a given CC (normal form cseg here). For cseg [0, 1, 3, 2],
        there are 2 instances of type +1 CI, 2 type +2 CI, 1. CIA =
        ([2, 2, 1], [1, 0, 0])

        'up_intervals' and 'down_intervals' store the contour intervals
        that the method counts.

        'combinations' stores all the elements combinations in cseg.

        The loop appends positive elements in ups_list and negative in
        downs_list.

        'ups' and 'downs' stores contour intervals counting for all
        types of positive and negative intervals in the cseg.
        """

        up_intervals = range(1, len(self.cseg))
        down_intervals = [(x * -1) for x in up_intervals]
        combinations = i.combinations(self.cseg, 2)
        ups_list = []
        downs_list = []

        for x in combinations:
            y = Contour(x).contour_interval()
            if y > 0:
                ups_list.append(y)
            elif y < 0:
                downs_list.append(y)
            else:
                pass

        ups = [ups_list.count(x) for x in up_intervals]
        downs = [downs_list.count(x) for x in down_intervals]

        return ups, downs

    def contour_class_vector_i(self):
        """Return Friedmann (1985) CCVI, a two-digit summation of
        degrees of ascent and descent expressed in contour interval
        array. The first digit is the total of products of frequency
        and contour interval types of up contour intervals, and the
        second, of down contour intervals. For example, in CIA([2, 2,
        1], [1, 0, 0], CCVI = [(2 * 1) + (2 * 2) + (1 * 3)], [(1 * 1),
        (2 * 0), (3 * 0)]. So, CCVI = [5, 1].

        'items' stores the contour intervals to be sum.

        'up_list' and 'down_list' stores the up and down contour
        interval frequency lists.

        'up_sum' and 'down_sum' stores the sum of the product of each
        contour interval frequency and contour interval value.
        """

        items = range(1, len(self.cseg))
        up_list, down_list = self.contour_interval_array()
        up_sum = sum([(a * b) for a, b in i.izip(up_list, items)])
        down_sum = sum([(a * b) for a, b in i.izip(down_list, items)])
        return [up_sum, down_sum]

    def contour_class_vector_ii(self):
        """Return Friedmann (1985) CCVII, a two-digit summation of
        degrees of ascent and descent expressed in contour interval
        array. The first digit is the total of frequency of up contour
        intervals, and the second, of down contour intervals. For
        example, in CIA([2, 2, 1], [1, 0, 0], CCVII = [5, 1]."""

        return [sum(x) for x in self.contour_interval_array()]

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


def ri_identity_test(cseg):
    """Returns 1 if cseg have identity under retrograde inversion."""

    return 1 if cseg == Contour(Contour(cseg).retrograde()).inversion() else 0


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
