#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import collections
from collections import MutableSequence
from copy import deepcopy
import operator
import __utils as utils
import __auxiliary as auxiliary
import diagonal
import matrix
import fuzzy


class ContourPointException(Exception):
    pass


class ContourException(Exception):
    pass


def build_classes_card(card, prime_algorithm="prime_form_marvin_laprade"):
    """Generates contour classes like Marvin and Laprade (1987) table
    for one cardinality. Accepts more than one algorithm of prime
    form. Marvin and Laprade algorithm is default.
    Returns (card, number, contour class).

    >>> build_classes_card(3, 'prime_form_sampaio')
    [(3, 1, (0, 1, 2), True), (3, 2, (0, 2, 1), False)]
    """

    def __tuple_prime(lst, prime_algorithm):
        """Returns a tuple with a cseg from a list of c-pitches.

        >>> __tuple_prime([2, 1, 0])
        (0, 1, 2)
        """

        return tuple(auxiliary.apply_fn(Contour(lst), prime_algorithm).cseg)

    def __single_class_build(card, class_n, cseg):
        """Returns a single contour class from cardinality, class
        number, and cseg.

        >>> __single_class_build(4, 1, (0, 1, 3, 2))
        (4, 2, (0, 1, 3, 2), False)
        """

        return card, class_n + 1, cseg, Contour(list(cseg)).ri_identity_test()

    permut = auxiliary.permut_csegs(card)
    primes_repeats = [__tuple_prime(el, prime_algorithm) for el in permut]
    primes = enumerate(sorted(list(set(primes_repeats))))

    return [__single_class_build(card, n, x) for n, x in primes]


def build_classes(cardinality, prime_algorithm="prime_form_marvin_laprade"):
    """Generates contour classes like Marvin and Laprade (1987)
    table. Accepts more than one algorithm of prime form. Marvin and
    Laprade algorithm is default.

    >>> build_classes_card(3, 'prime_form_sampaio')
    [[(2, 1, (0, 1), True)],
    [(3, 1, (0, 1, 2), True), (3, 2, (0, 2, 1), False)],
    [(4, 1, (0, 1, 2, 3), True),
    (4, 2, (0, 1, 3, 2), False),
    (4, 3, (0, 2, 1, 3), True),
    (4, 4, (0, 2, 3, 1), False),
    (4, 5, (0, 3, 1, 2), False),
    (4, 6, (0, 3, 2, 1), False),
    (4, 7, (1, 0, 3, 2), True),
    (4, 8, (1, 3, 0, 2), True)]]
    """

    card_list = range(2, (cardinality + 1))
    return [build_classes_card(c, prime_algorithm) for c in card_list]


def pretty_classes(cardinality, prime_algorithm="prime_form_marvin_laprade"):
    """Returns contour classes like Marvin and Laprade (1987)
    table. Accepts more than one algorithm of prime form. Marvin and
    Laprade algorithm is default.

    'cc' stores flatten contour classes of all cardinalities until the
    one given.
    """

    header = "C-space segment-classes [based on Marvin and Laprade (1987)]" + \
             "\n{0}".format("-" * 60) + \
             "\n* indicates identity under retrograde inversion.\n" + \
             "{0}\n".format("=" * 60)

    sec_txt = "\nC-space segment classes for cseg cardinality "
    sections = []

    cc = utils.flatten(build_classes(cardinality, prime_algorithm))
    card = 0
    for a, b, c, d in [[a, b, c, d] for (a, b, c, d) in cc]:
        if a != card:
            sections.append(sec_txt + "{0}\n".format(a))
            sections.append("\n" + " ".ljust(1) + "Csegclass".ljust(18) +
                  "Prime form".ljust(20) + "INT(1)\n")
            card = a
        if d:
            ri = "*"
        else:
            ri = " "
        csegclass = Contour(c)
        int_diagonals = Contour(c).internal_diagonals(1)
        str_int_diag = diagonal.InternalDiagonal(int_diagonals)
        sections.append(" ".ljust(4) +
                        "c {0}-{1}{2}".format(a, b, ri).ljust(16) +
                        str(csegclass).ljust(20) +
                        str(str_int_diag).ljust(15) + "\n")
    return header + "".join(sections)


def contour_class(cardinality, number):
    """Returns the prime form of a given contour class.

    >>> contour_class(6, 117)
    < 0 5 4 2 1 3 >
    """

    for (card, n, cseg, ri) in build_classes_card(cardinality):
        if card == cardinality and n == number:
            return Contour(cseg)


def subsets_grouped(dictionary, group_type):
    """Returns a string with subsets grouped by their group type.

    If the group type is normal form, input list must be the
    Contour.subsets_normal output. If the group type is prime form,
    input list must be the Contour.subsets_prime output.

    >>> subsets_grouped([[[1, 3, 0, 2], [3, 1, 4, 2]],
                        [[0, 2, 3, 1], [0, 3, 4, 2]]], 'prime')
    'Prime form < 1 3 0 2 > (1)\n< 3 1 4 2 >\n' + \
    '\nPrime form < 0 2 3 1 > (1)\n< 0 3 4 2 >'
    """

    text = "{0} form".format(group_type).capitalize()
    dic = dictionary
    r = []
    keys = [[len(i), i] for i in dic.keys()]
    keys.sort()
    keys = [x[1] for x in keys]
    for key in keys:
        r.append("{0} {1} ({2})".format(text, Contour(list(key)),
                                        len(dic[key])))
        r.append("\n".join([str(Contour(x)) for x in dic[key]]))
    return "\n".join(r)


def maxima(el1, el2, el3):
    """Tests if a given 3 element has maxima (Morris, 1993).

    >>> maxima(1, 3, 2)
    True
    """

    return el1 <= el2 >= el3


def minima(el1, el2, el3):
    """Tests if a given 3 element has minima (Morris, 1993).

    >>> minima(1, 3, 2)
    False
    """

    return el1 >= el2 <= el3


def sort_cseg_seq(cseg_objs):
    """Returns a list of ContourPoints sorted by cseg."""

    result = sorted([(cseg_obj.cseg, cseg_obj) for cseg_obj in cseg_objs])
    return [x[1] for x in result]


def repeated_cps_value_group(cpoints):
    """Returns sequences of adjacent cpoints with repeated values.
    (Morris 1993)

    >>> Contour([0, 2, 2, 2, 1])
    [< Position: 1, Value: 2 >, < Position: 2, Value: 2 >, < Position: 3, Value: 2 >]
    """

    obj_cseg = Contour(cpoints)

    # make list only if there are repeated adjacent cpoints values
    if obj_cseg.repetition_adjacent_cpitch_test():
        pairs = [(cpoint.position, cpoint.value) for cpoint in cpoints]
        grouped = itertools.groupby(pairs, key=operator.itemgetter(1))
        group = [list(items[1]) for items in grouped]
        return [[obj_cseg.cpoint_by_position(subseq[0]) for subseq in seq] for seq in group]
    else:
        return cpoints


def reduction_retention(cpoints):
    """Returns medial cps value if it is maxima or minima of a given
    list with an even number of consecutive cps. (Bor, 2009)

    >>> reduction_retention([None, 0, 2, 1, 2])
    2
    """

    def aux_max_min(cpoints, fn):
        result = []
        for cpoint in cpoints:
            try:
                result.append(cpoint.value)
            except:
                pass
        return fn(result)

    def aux_cond(seq):
        try:
            return list(set(seq)) == [None]
        except:
            return False

    size = len(cpoints)
    if size % 2 == 0:
        print "Error. 'cpoints' must be a sequence with an even number of elements."
    else:
        cpoints_max = aux_max_min(cpoints, max)
        cpoints_min = aux_max_min(cpoints, min)

        medial_pos = size / 2
        medial = cpoints[medial_pos]
        left_seq = cpoints[:medial_pos]
        right_seq = cpoints[medial_pos + 1:]

        # retain if medial is the first or last el
        if aux_cond(left_seq) or aux_cond(right_seq):
            return medial
        # repeations. Do not retain if medial is the second
        # consecutive repeated cps
        elif medial.value == cpoints[medial_pos - 1].value:
            return None
        # retain if medial is max or min
        elif medial.value == cpoints_max or medial.value == cpoints_min:
            return medial
        else:
            return None


def contour_rotation_classes(cardinality):
    """Returns all rotation related contour classes of a given
    cardinality. Each cseg is rotation class representative.

    >>> contour_rotation_classes(4)
    [< 0 1 2 3 >, < 0 1 3 2 >, < 0 2 1 3 >]
    """

    # sets universe set with all csegs with a given cardinality
    universe = set([tuple(x) for x in auxiliary.permut_csegs(cardinality)])
    s = set()

    for el in universe:
        obj_cseg = Contour(el)
        representatives = obj_cseg.rotated_representatives()
        all_el = set([tuple(x.cseg) for x in representatives])
        r = 0
        # tests if an operation in cseg's all operation is already in
        # s set
        for op in all_el:
            if op in s:
                r += 1
        if r == 0:
            s.update([el])

    # sets the first contour of each class for function return
    result = []

    for el in s:
        obj_cseg = Contour(el)
        all_el = [Contour(x) for x in obj_cseg.rotated_representatives()]
        result.append(sort_cseg_seq(all_el)[0])

    return sort_cseg_seq(result)


class ContourPoint():
    """Returns an object contourpoint.
    Input is a pair of position and value:

    >>> ContourPoint(0, 2)
    < Position: 0, Value: 2 >
    """

    def __init__(self, position, value, maxima=False, minima=False):
        if not all([isinstance(x, int) for x in value, position]):
            raise ContourPointException("Cpoint position and value must be integers.", position, value)
        self.position = position
        self.value = value
        self.cpoint = (position, value)
        self.maxima = maxima
        self.minima = minima

    def __eq__(self, other):
        if not isinstance(other, ContourPoint):
            return False
        try:
            return all([self.cpoint == other.cpoint, self.maxima == other.maxima, self.minima == other.minima])
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "< Position: {0}, Value: {1} >".format(self.position, self.value)
    def flag(self, fn):
        """Returns a flagged cpoint with maxima, minima or both."""

        cpoint = deepcopy(self)
        if fn == maxima:
            cpoint.maxima = True
        elif fn == minima:
            cpoint.minima = True
        elif fn == 'Both':
            cpoint.maxima = cpoint.minima = True
        return cpoint

    def unflag(self, fn):
        """Returns a cpoint with unflagged attribute maxima, minima or
        both."""

        cpoint = deepcopy(self)
        if fn == maxima:
            cpoint.maxima = False
        elif fn == minima:
            cpoint.minima = False
        elif fn == 'Both':
            cpoint.maxima = cpoint.minima = False
        return cpoint


class Contour(MutableSequence):
    """Returns an object contour.
    Input is a list of cpoints, or a list of objects ContourPoints:

    >>> Contour([0, 1, 3, 2])
    < 0 1 3 2 >
    """

    def __init__(self, cpoints):
        if all([isinstance(item, ContourPoint) for item in cpoints]):
            self.cpoints = cpoints
        else:
            if any([isinstance(cpoint, float) for cpoint in cpoints]):
                cpoints = [sorted(set(cpoints)).index(x) for x in cpoints]
            try:
                self.cpoints = [ContourPoint(pos, val) for pos, val in enumerate(cpoints)]
            except:
                raise ContourException("Don't know how to handle the input: " + cpoints)

        self.cseg = [cpoint.value for cpoint in self.cpoints]
        self.positions = [cpoint.position for cpoint in self.cpoints]
        self.size = len(self.cseg)

    def __repr__(self):
        return "< {0} >".format(" ".join([str(x) for x in self.cseg]))

    def __eq__(self, other):
        if not isinstance(other, Contour):
            return False
        try:
            if len(self.cpoints) == len(other.cpoints):
                return all(x == y for x, y in zip(self.cpoints, other.cpoints))
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __delitem__(self, i):
        del self.cpoints[i]

    def __getitem__(self, i):
        return self.cpoints[i]

    def __len__(self):
        return len(self.cpoints)

    def __setitem__(self, i, value):
        self.cpoints[i] = value

    def __add__(self, other):
        return Contour(self.cpoints + other.cpoints)

    def insert(self, i, value):
        self.cpoints.insert(i, value)

    def rotation(self, factor=1):
        """Rotates a cseg around a factor.

        factor is optional. Default factor=1.

        'n' is the module of input factor. It's allowed to use factor
        numbers greater than cseg size.

        >>> Contour([0, 1, 2, 3]).rotation(2)
        < 2 3 0 1 >
        """

        cseg = self.cseg
        n = factor % self.size

        return Contour(cseg[n:] + cseg[:n])

    def retrogression(self):
        """Returns contour retrograde.

        >>> Contour([0, 1, 2, 3]).retrogression()
        < 3 2 1 0 >
        """

        return Contour(self.cseg[::-1])

    def inversion(self):
        """Returns contour inversion.

        >>> Contour([0, 3, 1, 2]).inversion()
        < 3 0 2 1 >
        """

        cseg = self.cseg
        return Contour([(max(cseg) - cps) for cps in cseg])

    def translation(self):
        """Returns the normal form (Marvin 1987) of a given contour.
        It's the same of Friedmann (1985, 1987) contour class (CC).

        >>> Contour([4, 2, 6, 1]).translation()
        < 2 1 3 0 >
        """

        cseg = self.cseg
        return Contour([sorted(set(cseg)).index(x) for x in cseg])

    def cpoint(self, position):
        """Returns ContourPoint in a given index position."""

        try:
            return self.cpoints[position]
        except:
            print "The cseg size in this contour object is smaller than", position

    def cpoint_by_position(self, position):
        """Returns ContourPoint with a given position."""

        cpoints = self.cpoints
        try:
            return [cpoint for cpoint in cpoints if cpoint.position == position][0]
        except:
            print "This contour object doesn't have position", position

    def reset(self):
        """Reset original flags and reenumerate positions from 0 to n
        - 1, where n is contour object cardinality.
        """

        def remake(position, cpoint):
            """Returns a ContourPoint with a given position number and without
            flags."""

            return ContourPoint(position, cpoint.value)

        cpoints = self.cpoints
        e_cpoints = enumerate(cpoints)
        cpoints = [remake(position, cpoint) for position, cpoint in e_cpoints]

        return Contour(cpoints)

    def repetition_cpitch_test(self):
        """Returns True if cseg has repeated elements."""

        return self.size != len(set([x for x in self.cseg]))

    def repetition_adjacent_cpitch_test(self):
        """Tests if cseg has any adjacent repeated elements."""

        cseg = self.cseg
        size = self.size
        return any([True if cseg[i - 1] == cseg[i] else False for i in range(1, size)])

    def remove_repeated_adjacent_cps(self):
        """Remove adjacent repeated cpoints in a given cseg."""

        cpoints = deepcopy(self.cpoints)

        new_cpoints = [cpoints[0]]

        # remove non-repeated adjacent cpoint. keep the first, remove
        # repetition
        for cpoint in cpoints:
            if cpoint.value != new_cpoints[-1].value:
                new_cpoints.append(cpoint)

        return Contour(new_cpoints)

    def __unequal_edges(self):
        """Returns the first cps position with different value from
        its symmetric. For instance, given a cseg C [0, 3, 1, 4, 2, 3,
        0], the first cps with different value for its symmetric is
        C_2 = 1.
        C_0 == C_-1
        c_1 == C_-2
        c_2 != C_-3
        So, the function returns cpitch position: 2.
        """

        cseg = self.cseg
        for position in range(self.size / 2):
            if cseg[position] != cseg[utils.negative(position) - 1]:
                return position

    def __prime_form_marvin_laprade_step_2(self, position):
        """Runs Marvin and Laprade (1987) second step of prime form
        algorithm.

        If (n - 1) - last pitch < first pitch, invert.

        position: the first cps position that its value is different
        for its symmetric (cf. unequal_edges).
        """

        reduced = self

        # if first and last cps are equal, the second must be compared
        # to penultimate cps and so on to break the "tie".

        false_first = self.cpoint(position).value
        false_last = self.cpoint(utils.negative(position) - 1).value

        if ((self.size - 1) - false_last) < false_first:
            reduced = self.inversion()

        return reduced

    def __prime_form_marvin_laprade_step_3(self, position):
        """Runs Marvin and Laprade (1987) third step of prime form
        algorithm.

        If last cpitch < first cpitch, retrograde.

        position: the first cps position that its value is different
        for its symmetric (cf. unequal_edges).
        """

        reduced = self

        false_first = self.cpoint(position).value
        false_last = self.cpoint(utils.negative(position) - 1).value

        if false_last < false_first:
            reduced = self.retrogression()

        return reduced

    def __non_repeated_prime_form_marvin_laprade(self):
        """Returns the prime form of a given contour (Marvin and
        Laprade, 1987)."""

        # the first cps position that its value is different for its
        # symmetric (cf. unequal_edges).
        position = self.__unequal_edges()

        # step 1: translate if necessary
        step1 = self.translation()
        step2 = step1.__prime_form_marvin_laprade_step_2(position)
        step3 = step2.__prime_form_marvin_laprade_step_3(position)

        return step3

    def __repeated_prime_generic(self, prime_algorithm):
        """Returns prime forms of a repeated cpitch cseg calculated
        with a given prime_algorithm.
        """

        triangle = self.comparison_matrix().superior_triangle()
        csegs = matrix.triangle_zero_replace_to_cseg(triangle)

        return [auxiliary.apply_fn(c, prime_algorithm) for c in csegs]

    def prime_form_marvin_laprade(self):
        """Returns the prime form of a given contour (Marvin and
        Laprade, 1987).

        >>> Contour([4, 2, 6, 1]).prime_form_marvin_laprade()
        < 0 3 1 2 >
        """

        cseg = self.cseg
        if not self.repetition_cpitch_test():
            return self.__non_repeated_prime_form_marvin_laprade()
        else:
            # Returns prime forms of a repeated cpitch cseg.
            return self.__repeated_prime_generic("prime_form_marvin_laprade")

    def prime_form_sampaio(self):
        """Runs Sampaio prime form algorithm.

        The Sampaio prime form algorithm returns the csegclass
        representative with the best ascendent numeric order.

        >>> Contour([0, 2, 1, 3, 4]).prime_form_sampaio()
        < 0 1 3 2 4 >
        """

        # tests if cseg has repeated elements
        if not self.repetition_cpitch_test():
            # Returns Sampaio prime form algorithm for non repeated
            # c-pitches csegs.

            # The Sampaio prime form algorithm returns the csegclass
            # representative with the best ascendent numeric order.
            return sort_cseg_seq(self.class_four_forms())[0]
        else:
            # Returns Sampaio prime form algorithm for repeated
            # c-pitches csegs.

            # Returns all possible prime forms of a cseg with repeated
            # elements
            return self.__repeated_prime_generic("prime_form_sampaio")

    def unique_prime_form_test(self, prime_algorithm="prime_form_sampaio"):
        """Returns True if the prime form algorithm returns only one
        prime form for each contour class. Sampaio prime form
        algorithm is default.

        >>> Contour([0, 2, 1, 3, 4]).unique_prime_form_test()
        True
        """

        p, i, r, ri = self.class_representatives()

        prime_p = auxiliary.apply_fn(p, prime_algorithm)
        prime_i = auxiliary.apply_fn(i, prime_algorithm)
        prime_r = auxiliary.apply_fn(r, prime_algorithm)
        prime_ri = auxiliary.apply_fn(ri, prime_algorithm)

        return prime_p == prime_i == prime_r == prime_ri

    def subsets(self, n):
        """Returns adjacent and non-adjacent subsets of a given
        contour.

        >>> Contour([0, 2, 1, 3, 4]).subsets(4)
        [< 0 1 3 4 >, < 0 2 1 3 >, < 0 2 1 4 >, < 0 2 3 4 >, < 2 1 3 4 >]
        """

        n_combinations = itertools.combinations(self.cseg, n)

        return [Contour(x) for x in sorted([el for el in n_combinations])]

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

        for obj_cseg in subsets:
            cseg_tuple = tuple(obj_cseg.translation().cseg)
            if cseg_tuple in dic:
                z = dic[cseg_tuple]
                z.append(obj_cseg)
                dic[cseg_tuple] = z
            else:
                dic[cseg_tuple] = [obj_cseg]

        return dic

    def subsets_prime(self, n, prime_algorithm="prime_form_sampaio"):
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

        for obj_cseg in subsets:
            process = tuple(auxiliary.apply_fn(obj_cseg, prime_algorithm).cseg)
            if process in dic:
                z = dic[process]
                z.append(obj_cseg)
                dic[process] = z
            else:
                dic[process] = [obj_cseg]

        return dic

    def all_subsets(self):
        """Returns adjacent and non-adjacent subsets of a given
        contour.

        >>> Contour([0, 1, 2]).all_subsets()
        [< 0 1 >, < 0 2 >, < 1 2 >, < 0 1 2 >]
        """

        sizes = range(2, self.size + 1)
        return utils.flatten([self.subsets(x) for x in sizes])

    def all_subsets_prime(self, prime_algorithm="prime_form_sampaio"):
        """Returns all adjacent and non-adjacent subsets of a given
        contour grouped by their prime forms.

        >>> Contour([0, 1, 2]).all_subsets_prime()
        {(0, 1): [< 0 1 >, < 0 2 >, < 1 2 >], (0, 1, 2): [< 0 1 2 >]}
        """

        sizes = range(2, self.size + 1)
        subsets_list = [self.subsets_prime(x, prime_algorithm) for x in sizes]
        [subsets_list[0].update(dic) for dic in subsets_list]
        return subsets_list[0]

    def all_subsets_normal(self):
        """Returns all adjacent and non-adjacent subsets of a given
        contour grouped by their normal forms.

        >>> Contour([0, 1, 3, 2]).all_subsets_normal()
        {(0, 1): [< 0 1 >, < 0 2 >, < 0 3 >, < 1 2 >, < 1 3 >],
        (0, 1, 2): [< 0 1 2 >, < 0 1 3 >],
        (0, 1, 3, 2): [< 0 1 3 2 >],
        (0, 2, 1): [< 0 3 2 >, < 1 3 2 >],
        (1, 0): [< 3 2 >]}
        """

        sizes = range(2, self.size + 1)
        subsets_list = [self.subsets_normal(x) for x in sizes]
        [subsets_list[0].update(dic) for dic in subsets_list]
        return subsets_list[0]

    def subsets_adj(self, n):
        """Returns adjacent n-elements subsets of a given contour.

        >>> Contour([0, 1, 3, 2]).subsets_adj()
        [< 0 1 3 >, < 1 3 2 >]
        """

        irange = range(self.size - (n - 1))
        return [Contour(self.cseg[i:i + n]) for i in irange]

    def cpoint_replace(self, old, new):
        """Replace a cpoint in a contour object by a given cpoint."""

        obj_cseg = deepcopy(self)
        try:
            obj_cseg[obj_cseg.index(old)] = new
            return obj_cseg
        except:
            raise IndexError("Given old cpoint doesn't belong to given contour object")

    def cpoint_flag(self, cpoint, flag, unflag=False):
        """Flag or unflag a given cpoint in a contour object with a
        given flag. Flag must be maxima, minima or 'Both'."""

        obj_cseg = deepcopy(self)
        if unflag:
            flagged_cpoint = cpoint.unflag(flag)
        else:
            flagged_cpoint = cpoint.flag(flag)
        return obj_cseg.cpoint_replace(cpoint, flagged_cpoint)

    def max_min_flag(self):
        """Returns contour object with flagged maxima and minima
        (Morris, 1993).

        >>> Contour([0, 1, 2]).max_min_flag()
        < 0 1 2 >
        """

        def fn_test(cpoints, i, fn):
            """Test if given cpoint of 'i' index in cpoints is maxima
            or minima (fn)."""

            return fn(*[cp.value for cp in cpoints[i - 1:i + 2]])

        def aux_flag(obj_cseg, max_min_list, fn):
            """Returns contour object with flagged/unflagged maxima,
            minima cpoints."""

            for i in range(1, len(max_min_list) - 1):
                cpoint = max_min_list[i]
                if fn_test(max_min_list, i, fn):
                    obj_cseg = obj_cseg.cpoint_flag(cpoint, fn)
                else:
                    obj_cseg = obj_cseg.cpoint_flag(cpoint, fn, True)

            return obj_cseg

        obj_cseg = deepcopy(self)
        cpoints = obj_cseg.cpoints

        # tests if obj_cseg has maxima or minima previously defined
        first = cpoints[0]
        if all([first.maxima, first.minima]):
            max_list = [cpoint for cpoint in cpoints if cpoint.maxima]
            min_list = [cpoint for cpoint in cpoints if cpoint.minima]
            obj_cseg = aux_flag(obj_cseg, max_list, maxima)
            obj_cseg = aux_flag(obj_cseg, min_list, minima)
        else:
            # first and last are flagged by default (Morris, 1993)
            obj_cseg = obj_cseg.cpoint_flag(cpoints[0], 'Both')
            obj_cseg = obj_cseg.cpoint_flag(cpoints[-1], 'Both')
            obj_cseg = aux_flag(obj_cseg, cpoints, maxima)
            obj_cseg = aux_flag(obj_cseg, obj_cseg.cpoints, minima)

        return obj_cseg

    def unflagged_test(self):
        """Tests if a given contour object has unflagged cpoints."""

        return not all([any([cpoint.maxima, cpoint.minima]) for cpoint in self.cpoints])

    def unflagged_remove(self):
        """Returns a contour object with all unflagged cpoints
        removed. (Morris, 1993)

        >>> Contour([ContourPoint(0, 1, True, True),
                     ContourPoint(1, 1),
                     ContourPoint(2, 2, True, True)])
        < 0 2 >
        """

        def aux_max_min_test(cpoint):
            return any(x for x in [cpoint.maxima, cpoint.minima])

        obj_cseg = deepcopy(self)
        cpoints = obj_cseg.cpoints

        return Contour([cpoint for cpoint in cpoints if aux_max_min_test(cpoint)])

    def repeated_cpoint_flag(self):
        """Returns a contour object with ajdacent repeated cpoints
        (un)flagged by Morris algorithm steps 6 and 7 (Morris, 1993).
        """

        def add(cpoint, new_cpoints, fn=None):
            if fn is not None:
                cpoint = cpoint.unflag(fn)
            new_cpoints.append(cpoint)

        def aux_extremes(group, extremes):
            # tests if first or last cpoints are in group
            return any([extreme in group for extreme in extremes])

        def aux_remove(repeated_group, extremes, fn):
            new_cpoints = []
            for group in repeated_group:
                if len(group) > 1:
                    # maximum and/or minimum in string: flag only it
                    if aux_extremes(group, extremes):
                        [add(cpoint, new_cpoints) if cpoint in extremes else add(cpoint, new_cpoints, fn) for cpoint in group]

                    # not maximum neither minimum in string: flag only one
                    # of them (I choose the first one)
                    else:
                        add(group[0], new_cpoints)
                        [add(cpoint, new_cpoints, fn) for cpoint in group[1:]]
                else:
                    new_cpoints.append(group[0])

            return new_cpoints

        obj_cseg = deepcopy(self)
        cpoints = obj_cseg.cpoints

        first = cpoints[0]
        last = cpoints[-1]
        extremes = [first, last]

        # Flag all maxima (step 6) and minima (step 7)
        max_min_list = obj_cseg.max_min_flag()

        # if max_min_list has cpoint value adjacent repetitions, then:
        # regroup max_min_list by adjcent repeated value cpoints
        if max_min_list.repetition_adjacent_cpitch_test():
            repeated_group = repeated_cps_value_group(max_min_list)
            new_cpoints = aux_remove(repeated_group, extremes, maxima)
            new_repeated = repeated_cps_value_group(new_cpoints)
            new_cpoints = aux_remove(new_repeated, extremes, minima)
        else:
            new_cpoints = max_min_list

        return Contour(new_cpoints)

    def reduction_morris(self, reset=True, translation=True):
        """Returns Morris (1993) contour reduction from a cseg, and
        its depth.

        >>> Contour([0, 4, 3, 2, 5, 5, 1]).reduction_morris()
        [< 0 2 1 >, 2]
        """

        obj_cseg = deepcopy(self)

        # Given a contour C and variable n
        # step 0. n = 0 (depth)
        n = 0

        # steps 1 and 2. flag all maxima/minima in C
        max_min_list = obj_cseg.max_min_flag()

        # step 3. test if C has unflagged pitches.
        # if all pitches in C are flagged, go to step 9
        unflagged = max_min_list.unflagged_test()

        while unflagged:
            # step 4: delete all non-flagged pitches in c
            max_min_list = max_min_list.unflagged_remove()

            # step 5: n is incremented by 1
            n += 1

            # steps 6 and 7:
            max_min_list = max_min_list.repeated_cpoint_flag()

            # step 8
            unflagged = max_min_list.unflagged_test()

        # step 9
        reduced = max_min_list

        # outside algorithm: returns reset and/or translated
        if reset:
            reduced = reduced.reset()
        if translation:
            reduced = reduced.translation()

        return [reduced, n]

    def reduction_window(self, window_size=3, translation=True, reposition=True):
        """Returns a reduction in a single turn of n-window reduction
        algorithm. (Bor, 2009). If translation is true, the method
        returns a translated object. If reposition is true, the method
        returns an object with positions from 0 to n - 1, where n is
        cseg cardinality.

        >>> Contour([7, 10, 9, 0, 2, 3, 1, 8, 6, 2, 4, 5]).reduction_window(3, False)
        < 7 10 0 3 1 8 2 5>
        """

        def _red(cpoints, pos, window_size):
            return reduction_retention(cpoints[pos:pos + window_size])

        if window_size % 2 == 0:
            print "Window size must be an even number."
        else:
            cpoints = deepcopy(self.cpoints)
            n = window_size / 2

            for i in range(n):
                cpoints.insert(0, None)
                cpoints.append(None)

            size = len(cpoints)
            last = size - window_size + 1
            prange = range(0, last)

            reduced = Contour([_red(cpoints, pos, window_size) for pos in prange if _red(cpoints, pos, window_size)])

            if translation:
                reduced = reduced.translation()

            if reposition:
                reduced = Contour(reduced.cseg)

            return reduced

    def reduction_window_recursive(self, window_size=3, translation=True):
        """Returns a reduction of n-window reduction algorithm in all
        turns necessary to most reduction form. (Bor, 2009).

        >>> Contour([7, 10, 9, 0, 2, 3, 1, 8, 6, 2, 4, 5]).reduction_window_recursive(5, False)
        < 7 10 0 3 1 8 2 5>
        """

        old = self
        depth = 0
        while old.reduction_window(window_size, translation) != old:
            old = old.reduction_window(window_size, translation)
            depth += 1
        return [old, depth]

    def reduction_bor(self, windows=3, translation=True):
        """Returns reduction contour and its depth with given windows
        sequence (Bor, 2009).

        >>> Contour([0, 6, 1, 4, 3, 5, 2]).reduction_bor(53)
        [< 0 2 1 >, 2]
        """

        win_vals = [int(x) for x in str(windows)]
        obj_cseg = deepcopy(self)
        depth = 0
        for window in win_vals:
            new_obj = obj_cseg.reduction_window(window, translation)
            if obj_cseg != new_obj:
                depth += 1
            obj_cseg = new_obj
        return [obj_cseg, depth]

    def reduction_sampaio(self, windows=3, translation=True):
        """Returns reduction contour and its depth with given windows
        sequence. (Sampaio, ?)
        """

        # calculate initial reduced by Bor algorithm
        reduced, depth = self.reduction_bor(windows, translation)

        seq = deepcopy(reduced).cseg
        i = 2

        while i < len(seq) - 1:
            if seq[i] == seq[i - 2] and seq[i + 1] == seq[i - 1]:
                seq.pop(i)
                seq.pop(i)
            else:
                i += 1

        seq = Contour(seq)

        # increase depth value only if original cseg is reduced
        if self == seq:
            depth = 0
        elif depth == 0 and self != seq:
            depth = 1

        if translation:
            seq = seq.translation()

        return [seq, depth]

    def interval_succession(self):
        """Return Friedmann (1985) CIS, a series which indicates the
        order of Contour Intervals in a given CC (normal form cseg
        here).

        >>> Contour([1, 2, 3, 5, 4, 0]).interval_succession()
        [1, 1, 2, -1, -4]
        """

        cseg = self.cseg
        return utils.seq_operation(utils.difference, cseg)

    def absolute_intervals_sum(self):
        """Return the sum of absolute intervals in a cseg.

        >>> Contour([0, 1, 3, 2]).absolute_intervals_sum()
        4
        """

        return sum(map(abs, self.interval_succession()))

    def absolute_intervals_average(self):
        """Return an average value of absolute intervals sum. The
        result is divided by cseg size.

        >>> Contour([0, 1, 2, 3]).absolute_intervals_average()
        0.75
        """

        return self.absolute_intervals_sum() / float(self.size)

    def absolute_intervals_index(self):
        """Return an index value of absolute intervals sum. The
        result is divided by the number of all possible leaps in cseg.

        >>> Contour([0, 1, 2, 3]).absolute_intervals_index()
        0.5
        """

        def highest(seq):
            pool = collections.deque(sorted(seq))
            temp = collections.deque([pool.popleft(), pool.pop()])
            try:
                while pool:
                    if temp[0] < temp[-1]:
                        temp.append(pool.popleft())
                        temp.appendleft(pool.pop())
                    else:
                        temp.append(pool.pop())
                        temp.appendleft(pool.popleft())
            except IndexError:
                pass
            return Contour(list(temp)).absolute_intervals_sum()

        return self.absolute_intervals_sum() / float(highest(self.cseg))

    def internal_diagonals(self, n=1):
        """Returns Morris (1987) int_n. The first internal diagonal
        (int_1) is the same of Friedmann (1985, 1987) contour
        adjacency series (CAS).

        >>> Contour([0, 1, 3, 2]).internal_diagonals()
        < + + - >
        """

        matrix = self.comparison_matrix()
        int_m = itertools.imap(cmp, matrix, itertools.islice(matrix, n, None))
        int_d = [x for x in int_m if x != 0]
        return diagonal.InternalDiagonal(int_d)

    def comparison_matrix(self):
        """Returns Morris (1987) a cseg COM-Matrix.

        >>> Contour([0, 1, 3, 2]).comparison_matrix()
        0 + + +
        - 0 + +
        - - 0 -
        - - + 0
        """

        cseg = self.cseg
        cm = [[cmp(b, a) for b in cseg] for a in cseg]
        return matrix.ComparisonMatrix(cm)

    def fuzzy_membership_matrix(self):
        """Returns a Fuzzy membership matrix. Quinn (1997).

        >>> Contour([0, 1, 3, 2]).fuzzy_membership_matrix()
        0 1 1 1
        0 0 1 1
        0 0 0 0
        0 0 1 0
        """

        return fuzzy.FuzzyMatrix(utils.make_matrix(fuzzy.membership, self))

    def fuzzy_comparison_matrix(self):
        """Returns a Fuzzy comparison matrix. Quinn (1997).

        >>> Contour([0, 1, 3, 2]).fuzzy_comparison_matrix()
        0 1 1 1
        -1 0 1 1
        -1 -1 0 -1
        -1 -1 1 0
        """

        return fuzzy.FuzzyMatrix(utils.make_matrix(fuzzy.comparison, self))

    def adjacency_series_vector(self):
        """Returns Friedmann (1985) CASV, a two digit summation of ups
        and downs of a CAS (internal diagonal n=1 here). For example,
        [2, 1] means 2 ups and 1 down.

        'internal_diagonal' stores cseg internal diagonal, n = 1.

        'ups' stores the total number of ups

        'downs' stores the total number of downs

        >>> Contour([0, 1, 3, 2]).adjacency_series_vector()
        [2, 1]
        """

        internal_diagonal = self.internal_diagonals(1)
        ups = sum([(x if x > 0 else 0) for x in internal_diagonal])
        downs = sum([(x if x < 0 else 0) for x in internal_diagonal])
        return [ups, abs(downs)]

    def interval_array(self):
        """Return Friedmann (1985) CIA, an ordered series of numbers
        that indicates the multiplicity of each Contour Interval type
        in a given CC (normal form cseg here). For cseg < 0 1 3 2 >,
        there are 2 instances of type +1 CI, 2 type +2 CI, 1. CIA =
        ([2, 2, 1], [1, 0, 0])

        'up_intervals' and 'down_intervals' store the contour intervals
        that the method counts.

        The loop appends positive elements in ups_list and negative in
        downs_list.

        'ups' and 'downs' stores contour intervals counting for all
        types of positive and negative intervals in the cseg.

        >>> Contour([0, 1, 3, 2]).interval_array()
        ([2, 2, 1], [1, 0, 0])
        """

        up_intervals = range(1, self.size)
        down_intervals = map(utils.negative, up_intervals)
        ups_list = []
        downs_list = []

        for cpoints in itertools.combinations(self.cseg, 2):
            interval = utils.difference(*cpoints)
            if interval > 0:
                ups_list.append(interval)
            elif interval < 0:
                downs_list.append(interval)

        ups = [ups_list.count(up_i) for up_i in up_intervals]
        downs = [downs_list.count(down_i) for down_i in down_intervals]

        return ups, downs

    def class_vector_i(self):
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

        >>> Contour([0, 1, 3, 2]).class_vector_i()
        [9, 1]
        """

        items = range(1, self.size)
        up_list, down_list = self.interval_array()
        up_sum = sum([a * b for a, b in itertools.izip(up_list, items)])
        down_sum = sum([a * b for a, b in itertools.izip(down_list, items)])
        return [up_sum, down_sum]

    def class_vector_ii(self):
        """Return Friedmann (1985) CCVII, a two-digit summation of
        degrees of ascent and descent expressed in contour interval
        array. The first digit is the total of frequency of up contour
        intervals, and the second, of down contour intervals. For
        example, in CIA([2, 2, 1], [1, 0, 0], CCVII = [5, 1].

        >>> Contour([0, 1, 3, 2]).class_vector_ii()
        [5, 1]
        """

        return [sum(intervals) for intervals in self.interval_array()]

    def __class_index(self, vector_method):
        """Returns a general upward/downward decimal index, that -1.0
        means the cseg is completely downward; 1.0 means the cseg is
        completely upward, and 0 means the cseg is balanced. Accepts
        Friedmann CCVI and CCVII as vector method.

        >>> Contour([0, 3, 1, 2]).__class_index('class_vector_i')
        0.69999999999999996
        """

        ups, downs = auxiliary.apply_fn(self, vector_method)
        total = ups + downs
        if ups == downs:
            return 0
        elif ups > downs:
            return ups / float(total)
        else:
            return utils.negative(downs) / float(total)

    def class_index_i(self):
        """Returns a general upward/downward decimal index, that -1.0
        means the cseg is completely downward; 1.0 means the cseg is
        completely upward, and 0 means the cseg is balanced. This
        operation is based on Friedmann CCVI.

        >>> Contour([0, 3, 1, 2]).class_index_i()
        0.69999999999999996
        """

        return self.__class_index("class_vector_i")

    def class_index_ii(self):
        """Returns a general upward/downward decimal index, that -1.0
        means the cseg is completely downward; 1.0 means the cseg is
        completely upward, and 0 means the cseg is balanced. This
        operation is based on Friedmann CCVII.

        >>> Contour([0, 3, 1, 2]).class_index_ii()
        0.66666666666666663
        """

        return self.__class_index("class_vector_ii")

    def segment_class(self, prime_algorithm="prime_form_sampaio"):
        """Returns contour segment class of a given cseg.

        Output format is: (cardinality, number, cseg_class, identity
        under retrograded inversion), like (3, 1, (0, 1, 2), True).

        >>> Contour([0, 1, 3, 2]).segment_class()
        (4, 2, < 0 1 3 2 >, False)
        """

        prime_form = auxiliary.apply_fn(self, prime_algorithm)
        cseg_classes = utils.flatten(build_classes(self.size, prime_algorithm))
        for cardinality, number, cseg_class, ri_identity in cseg_classes:
            if tuple(prime_form.cseg) == cseg_class:
                r = cardinality, number, Contour(list(cseg_class)), ri_identity
                return r

    def ri_identity_test(self):
        """Returns True if cseg have identity under retrograded
        inversion.

        >>> Contour([0, 1, 3, 2]).ri_identity_test()
        False
        """

        i = self.inversion()
        ri = i.retrogression()
        return self.cseg == ri.cseg

    def symmetry_index(self):
        """Returns the symmetry index based on the edge symmetry of a
        contour. This method compares first cseg half of a given cseg
        and its inverted retrograde. Each c-pitch of both cseg half is
        compared and, if equal, the total number of similarities is
        increased by 1. This number is later divided by the total
        number of elements of the cseg half.

        >>> Contour([0, 1, 4, 2, 3, 5, 6]).symmetry_index()
        0.5
        """

        cseg = self.cseg
        ri = self.retrogression().inversion().cseg
        size_half = round(self.size / float(2))
        int_size_half = int(size_half)
        half_cseg = cseg[:int_size_half]
        half_ri = ri[:int_size_half]

        result = 0
        for a, b in zip(half_cseg, half_ri):
            if a == b:
                result += 1

        return result / size_half

    def class_representatives(self, prime_algorithm="prime_form_sampaio"):
        """Returns the four csegclass representatives (Marvin and
        Laprade 1987, p. 237): prime, inversion, and retrograded
        inversion.

        >>> Contour([0, 1, 3, 2]).class_representatives()
        [< 0 1 3 2 >, < 3 2 0 1 >, < 2 3 1 0 >, < 1 0 2 3 >]
        """

        p = auxiliary.apply_fn(self, prime_algorithm)
        i = p.inversion()
        r = p.retrogression()
        ri = r.inversion()

        return [p, i, r, ri]

    def class_four_forms(self):
        """Returns four csegclass representative forms. This method is
        similar to class_representatives, but the first cseg form is
        the normal, not prime form.

        >>> Contour([0, 1, 3, 2]).class_representatives()
        [< 0 1 3 2 >, < 3 2 0 1 >, < 2 3 1 0 >, < 1 0 2 3 >]
        """

        t = self.translation()
        i = t.inversion()
        r = t.retrogression()
        ri = i.retrogression()

        return [t, i, r, ri]

    def all_rotations(self):
        """Returns all rotations forms of a cseg:

        >>> Contour([0, 1, 3, 2]).all_rotations()
        [< 0 1 3 2 >, < 1 3 2 0 >, < 3 2 0 1 >, < 2 0 1 3 >, < 0 1 3 2 >]
        """

        return [self.rotation(n) for n in range(self.size + 1)]

    def rotated_representatives(self):
        """Returns a set with csegclass representatives of each
        rotation of a contour.

        >>> Contour([0, 1, 3, 2]).rotated_representatives()
        [< 0 1 3 2 >, < 0 2 3 1 >, < 1 0 2 3 >, < 1 3 2 0 >,
        < 2 0 1 3 >, < 2 3 1 0 >, < 3 1 0 2 >, < 3 2 0 1 >]
        """

        rot = self.all_rotations()
        result = [contour.class_representatives() for contour in rot]
        result = utils.flatten(result)
        result = set([tuple(x.cseg) for x in result])

        return sort_cseg_seq([Contour(x) for x in result])

    def base_three_representation(self):
        """Returns Base three Contour Description, by Polansky and
        Bassein (1992). The comparison between c-points returns 0, 1,
        or 2 if the second c-point is lower, equal or higher than the
        first, respectively. This method returns a list with
        comparison of all combinations of c-points.

        >>> Contour([0, 1, 3, 2]).base_three_representation()
        [[2, 2, 2], [2, 2], [0]]
        """

        cseg = self.cseg
        combinations = itertools.combinations(cseg, 2)

        def aux_list(base_3, self):
            r_size = range(self.size - 1, 0, -1)
            result = []
            n = 0
            for i in r_size:
                seq = base_3[n:n + i]
                result.append(seq)
                n += i
            return result

        ternary = [auxiliary.base_3_comparison(a, b) for a, b in combinations]

        return aux_list(ternary, self)

    def oscillation(self):
        """Returns number of direction changes of a given
        cseg. (Schmuckler, 1999).
        """

        int_1 = self.internal_diagonals()
        return sum([1 for i in range(len(int_1) - 1) if int_1[i] != int_1[i + 1]])

    def oscillation_index(self):
        """Returns index of direction changes of a given
        cseg. (Schmuckler, 1999).
        """

        return self.oscillation() / float(self.size - 1)


def prime_form_algorithm_test(card, prime_form_algorithm="prime_form_sampaio"):
    """Returns contour classes with two prime forms from a given
    cardinality and prime form algorithm.

    >>> prime_form_algorithm_test(5, 'prime_form_marvin_laprade')
    [< 0 1 3 2 4 >, < 0 2 1 3 4 >, < 0 2 3 1 4 >, < 0 3 1 2 4 >,
    < 1 0 4 2 3 >, < 1 2 0 4 3 >, < 1 2 4 0 3 >, < 1 4 0 2 3 >,
    < 3 0 4 2 1 >, < 3 2 0 4 1 >, < 3 2 4 0 1 >, < 3 4 0 2 1 >,
    < 4 1 3 2 0 >, < 4 2 1 3 0 >, < 4 2 3 1 0 >, < 4 3 1 2 0 >]
    """

    # creates a list of all possible lists
    lists = [auxiliary.permut_csegs(c) for c in range(2, card + 1)]
    lists = utils.flatten(lists)

    coll = set()

    for lst in lists:
        cseg = Contour(lst)
        if not cseg.unique_prime_form_test(prime_form_algorithm):
            c_class, n_class, x, ri = cseg.segment_class()
            coll.add((c_class, n_class))

    classes = sorted(list(coll))
    result = []

    if classes != []:
        for cls in classes:
            cseg = auxiliary.cseg_from_class_number(*cls)
            ri = Contour(cseg).retrogression().inversion()
            result.append([cls, cseg, ri])

    return result


def possible_cseg(base_3):
    """Returns a cseg from a base 3 sequence, if the cseg is possible
    (Polansky and Bassein 1992).

    >>> possible_cseg([2, 2, 2])
    < 0 1 2 >
    """

    seq = utils.flatten(base_3)
    size = len(seq)
    for x in itertools.product(range(size), repeat=3):
        cseg = Contour(x)
        if utils.flatten(cseg.base_three_representation()) == seq:
            return Contour(x)
    return "Impossible cseg"
