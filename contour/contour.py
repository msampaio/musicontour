#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from itertools import (permutations, combinations, izip)
from math import factorial
from collections import defaultdict
from utils import (flatten, replace_list_to_plus_minus, list_to_string,
                   remove_duplicate_tuples)
from auxiliary import permut_csegs

class ContourError(Exception):
    pass


def build_classes(cardinality):
    """Generates contour classes like Marvin and Laprade (1987)
    software."""

    def __build_classes_card(card):
        """Generates contour classes like Marvin and Laprade (1987)
        software for one cardinality.

        Returns (card, number, contour class).
        """

        permut = permut_csegs(card)
        primes_repeats = [tuple(Contour(x).prime_form()) for x in permut]
        primes = enumerate(sorted(list(set(primes_repeats))))
        return [(card, n + 1, x, Contour(list(x)).ri_identity_test()) for n, x in primes]

    card_list = range(2, (cardinality + 1))
    return [__build_classes_card(c) for c in card_list]


def print_contour_classes(cardinality):
    """Prints contour classes like Marvin and Laprade (1987).

    'cc' stores flatten contour classes of all cardinalities until the
    one given.
    """

    header = "C-space segment-classes [based on Marvin and Laprade (1987)]" + \
             "\n{0}".format("-" * 60) + \
             "\n* indicates identity under retrograde inversion.\n" + \
             "{0}\n".format("=" * 60)

    sec_txt = "\nC-space segment classes for cseg cardinality "
    sections = []

    cc = flatten(build_classes(cardinality))
    card = 0
    for a, b, c, d in [[a, b, c, d] for (a, b, c, d) in cc]:
        if a != card:
            sections.append(sec_txt + "{0}\n".format(a))
            sections.append("\n" + " ".ljust(1) + "Csegclass".ljust(18) +
                  "Prime form".ljust(20) + "INT(1)\n")
            card = a
        if d == True:
            ri = "*"
        else:
            ri = " "
        csegclass = Contour(c).str_print()
        int_diagonals = Contour(c).internal_diagonals(1)
        str_int_diag = Internal_diagonal(int_diagonals).str_print()
        sections.append(" ".ljust(4) +
                        "c {0}-{1}{2}".format(a, b, ri).ljust(16) +
                        csegclass.ljust(20) + str_int_diag.ljust(15) + "\n")
    return header + "".join(sections)


def subsets_grouped(dictionary, group_type):
    """Returns a string with subsets grouped by their group type.

    If the group type is normal form, input list must be the
    Contour.subsets_normal output. If the group type is prime form,
    input list must be the Contour.subsets_prime output.

    >>> subsets_grouped([[[1, 3, 0, 2], [3, 1, 4, 2]],
                        [[0, 2, 3, 1], [0, 3, 4, 2]]], \"prime\")

    \"Prime form < 1 3 0 2 > (1)\n< 3 1 4 2 >\n\" + \
    \"\nPrime form < 0 2 3 1 > (1)\n< 0 3 4 2 >\"
    """

    text = "{0} form".format(group_type).capitalize()
    dic = dictionary

    r = []
    keys = [[len(i), i] for i in dic.keys()]
    keys.sort()
    keys = [x[1] for x in keys]
    for key in keys:
        r.append("{0} {1} ({2})".format(text, Contour(list(key)).str_print(),
                                        len(dic[key])))
        r.append("\n".join([Contour(x).str_print() for x in dic[key]]))
    return "\n".join(r)


# FIXME: move to maxima
def max_min(list_of_tuples, fn):
    """Returns a list with the position of maximum or minimum
    cpitches of a cseg. Maximum or minimum function is defined in
    fn argument.

    'n' stores the number of elements that is evaluated.
    'r' means result.
    """

    n = 3
    list_range = range(len(list_of_tuples) - n + 1)
    m_list = [list_of_tuples[0]]

    [m_list.append(fn(list_of_tuples[i:i + n])) for i in list_range]
    m_list.append(list_of_tuples[-1])

    return [x for x in m_list if x]


def maxima(list_of_tuples):
    """Returns maxima (Morris, 1993) positions in a cseg."""

    def maximum(dur_list):
        """Returns the maximum (Morris, 1993) position of a three
        c-pitches set. The input data is a list of three tuples. Each
        tuple has the c-pitch and its position. """

        (el1, p1), (el2, p2), (el3, p3) = dur_list
        return (el2, p2) if el2 >= el1 and el2 >= el3 else ''

    return max_min(list_of_tuples, maximum)


def minima(list_of_tuples):
    """Returns minima (Morris, 1993) positions in a cseg."""

    def minimum(dur_list):
        """Returns the minimum (Morris, 1993) position of a three
        c-pitches set. The input data is a list of three tuples. Each
        tuple has the c-pitch and its position. """

        (el1, p1), (el2, p2), (el3, p3) = dur_list
        return (el2, p2) if el2 <= el1 and el2 <= el3 else ''

    return max_min(list_of_tuples, minimum)


# FIXME:
# class Fontour(list):
#     def __init__(self, *args):
#         list.__init__(self, args)

# FIXME:
# def __repr__(self):
#     return "<{0}>".format(self[:])

class Contour():
    """Returns an objcect contour.
    Input is a list of cpitches:

    >>> Contour([0, 1, 3, 2])
    """

    def rotation(self, factor=1):
        """Rotates a cseg around a factor.

        factor is optional. Default factor=1.

        'n' is the module of input factor. It's allowed to use factor
        numbers greater than cseg size.
        """

        n = factor % len(self.cseg)
        subset = self.cseg[n:]
        subset.extend(self.cseg[0:n])
        return subset

    def retrograde(self):
        """Returns contour retrograde."""

        self.cseg.reverse()
        return self.cseg

    def inversion(self):
        """Returns contour inversion."""

        maxim = max(self.cseg)
        return [(maxim - cps) for cps in self.cseg]

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

        groups = izip(self.cseg, self.cseg[1:])
        return [a for a, b in groups if a != b] + [self.cseg[-1]]

    def subsets(self, n):
        """Returns adjacent and non-adjacent subsets of a given
        contour."""

        cseg = self.cseg
        return sorted([list(x) for x in combinations(cseg, n)])

    def subsets_normal(self, n):
        """Returns adjacent and non-adjacent subsets of a given
        contour grouped by their normal forms.

        Output is a dictionary where the key is the normal form, and
        the attribute is csubsets list.

        >>> Contour([0, 3, 1, 4, 2]).subsets_normal()
        {(0, 1, 3, 2): [[0, 1, 4, 2]],
        (0, 2, 1, 3): [[0, 3, 1, 4]],
        (0, 2, 3, 1): [[0, 3, 4, 2]],
        (0, 3, 1, 2): [[0, 3, 1, 2]],
        (2, 0, 3, 1): [[3, 1, 4, 2]]}
        """

        subsets = self.subsets(n)
        dic = {}

        for x in subsets:
            processed = tuple(Contour(x).translation())
            if processed in dic:
                z = dic[processed]
                z.append(x)
                dic[processed] = z
            else:
                dic[processed] = [x]

        return dic

    def subsets_prime(self, n):
        """Returns adjacent and non-adjacent subsets of a given
        contour grouped by their prime forms.

        Output is a dictionary where the key is the prime form, and
        the attribute is csubsets list.

        >>> Contour([0, 3, 1, 4, 2]).subsets_prime()
        {(0, 1, 3, 2): [[0, 1, 4, 2]],
        (0, 2, 1, 3): [[0, 3, 1, 4]],
        (0, 2, 3, 1): [[0, 3, 4, 2]],
        (0, 3, 1, 2): [[0, 3, 1, 2]],
        (1, 3, 0, 2): [[3, 1, 4, 2]]}
        """

        subsets = self.subsets(n)
        dic = {}

        for x in subsets:
            processed = tuple(Contour(x).prime_form())
            if processed in dic:
                z = dic[processed]
                z.append(x)
                dic[processed] = z
            else:
                dic[processed] = [x]

        return dic

    def all_subsets(self):
        """Returns adjacent and non-adjacent subsets of a given
        contour."""

        sizes = range(2, len(self.cseg) + 1)
        return flatten([self.subsets(x) for x in sizes])

    def all_subsets_prime(self):
        """Returns all adjacent and non-adjacent subsets of a given
        contour grouped by their prime forms."""

        sizes = range(2, len(self.cseg) + 1)
        subsets_list = [self.subsets_prime(x) for x in sizes]
        [subsets_list[0].update(dic) for dic in subsets_list]
        return subsets_list[0]

    def all_subsets_normal(self):
        """Returns all adjacent and non-adjacent subsets of a given
        contour grouped by their normal forms."""

        sizes = range(2, len(self.cseg) + 1)
        subsets_list = [self.subsets_normal(x) for x in sizes]
        [subsets_list[0].update(dic) for dic in subsets_list]
        return subsets_list[0]

    def subsets_adj(self, n):
        """Returns adjacent n-elements subsets of a given contour."""

        return [self.cseg[i:i + n] for i in range(len(self.cseg) - (n - 1))]

    def cps_position(self):
        """Returns a tuple with c-pitch and its position for each
        c-pitch of a cseg done."""

        return [(self.cseg[p], p) for p in range(len(self.cseg))]

    def contour_reduction_algorithm(self):
        """Returns Morris (1993) contour reduction from a cseg."""

        cseg_dur = self.cps_position()

        max_tmp = [0, cseg_dur]
        min_tmp = [0, cseg_dur]

        n = 0
        m = 0

        def steps_count(list, fn, variable):
            while(list[-1] != list[-2]):
                variable = variable + 1
                list.append(fn(remove_duplicate_tuples(list[-1])))

        steps_count(max_tmp, maxima, n)
        steps_count(min_tmp, minima, m)

        max_tmp = max_tmp[-1]
        min_tmp = min_tmp[-1]

        times = max([n, m])
        max_min = sorted(flatten([max_tmp, min_tmp]), key=lambda x: x[1])
        c = Contour([x for (x, y) in remove_duplicate_tuples(max_min)])
        return [c.prime_form(), times]

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

        subsets = self.subsets_adj(2)
        return [Contour([x[0], x[-1]]).contour_interval() for x in subsets]

    def internal_diagonals(self, n):
        """Returns Morris (1987) int_n. The first internal diagonal
        (int_1) is the same of Friedmann (1985, 1987) contour
        adjacency series (CC)."""

        subsets = self.subsets_adj(n + 1)
        return [Contour([x[0], x[-1]]).comparison() for x in subsets]

    def comparison_matrix(self):
        """Returns Morris (1987) a cseg COM-Matrix."""

        size = len(self.cseg)
        r_size = range(size)
        m = [[a, b] for a in self.cseg for b in self.cseg]
        n = [m[(i * size):((i + 1) * size)] for i in range(size)]
        line = [self.cseg]
        [line.append([Contour(x).comparison() for x in n[r]]) for r in r_size]
        return line

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

        The loop appends positive elements in ups_list and negative in
        downs_list.

        'ups' and 'downs' stores contour intervals counting for all
        types of positive and negative intervals in the cseg.
        """

        up_intervals = range(1, len(self.cseg))
        down_intervals = [-x for x in up_intervals]
        ups_list = []
        downs_list = []

        for x in combinations(self.cseg, 2):
            y = Contour(x).contour_interval()
            if y > 0:
                ups_list.append(y)
            elif y < 0:
                downs_list.append(y)

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
        up_sum = sum([a * b for a, b in izip(up_list, items)])
        down_sum = sum([a * b for a, b in izip(down_list, items)])
        return [up_sum, down_sum]

    def contour_class_vector_ii(self):
        """Return Friedmann (1985) CCVII, a two-digit summation of
        degrees of ascent and descent expressed in contour interval
        array. The first digit is the total of frequency of up contour
        intervals, and the second, of down contour intervals. For
        example, in CIA([2, 2, 1], [1, 0, 0], CCVII = [5, 1]."""

        return [sum(x) for x in self.contour_interval_array()]

    def contour_segment_class(self):
        """Returns contour segment class of a given cseg.

        Output format is: (cardinality, number, cseg_class, identity
        under retrograde inversion), like (3, 1, (0, 1, 2), True).
        """

        prime_form = self.prime_form()
        cseg_classes = flatten(build_classes(len(self.cseg)))
        for (cardinality, number, cseg_class, ri_identity) in cseg_classes:
            if tuple(prime_form) == cseg_class:
                return cardinality, number, cseg_class, ri_identity

    def ri_identity_test(self):
        """Returns True if cseg have identity under retrograde inversion."""

        i = Contour(self.cseg).inversion()
        ri = Contour(i).retrograde()
        return self.cseg == ri

    def str_print(self):
        """Prints cseg like used in Contour theories:
        < 1 3 5 4 >
        """

        return "< " + list_to_string(self.cseg) + " >"

    def __init__(self, cseg):
        self.cseg = cseg
