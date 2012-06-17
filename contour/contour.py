#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import collections
import utils
import auxiliary
import diagonal
import matrix
import fuzzy

class ContourError(Exception):
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

        return tuple(auxiliary.apply_fn(Contour(lst), prime_algorithm))

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
        if d == True:
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


def maxima_pair(list_of_tuples):
    """Returns maxima (Morris, 1993) positions in a cseg.

    >>> maxima_pair([(0, 1), (1, 2), (2, 4), (4, 5), (3, 3)])
    [(0, 1), (4, 5), (3, 3)]
    """

    def maximum(dur_list):
        """Returns the maximum (Morris, 1993) position of a three
        c-pitches set. The input data is a list of three tuples. Each
        tuple has the c-pitch and its position.
        """

        (el1, p1), (el2, p2), (el3, p3) = dur_list
        return (el2, p2) if el2 >= el1 and el2 >= el3 else ''

    return max_min(list_of_tuples, maximum)


def minima_pair(list_of_tuples):
    """Returns minima (Morris, 1993) positions in a cseg.

    >>> minima_pair([(0, 1), (1, 2), (2, 4), (4, 5), (3, 3)])
    [(0, 1), (3, 3)]
    """

    def minimum(dur_list):
        """Returns the minimum (Morris, 1993) position of a three
        c-pitches set. The input data is a list of three tuples. Each
        tuple has the c-pitch and its position.
        """

        (el1, p1), (el2, p2), (el3, p3) = dur_list
        return (el2, p2) if el2 <= el1 and el2 <= el3 else ''

    return max_min(list_of_tuples, minimum)


def reduction_retention(els):
    """Returns medial cps value if it is maxima or minima of a given
    list with an even number of consecutive cps. (Bor, 2009)

    >>> reduction_retention([None, 0, 2, 1, 2])
    2
    """

    size = len(els)
    if size % 2 == 0:
        print "Error. 'els' must be a sequence with an even number of elements."
    else:
        els_max = max(els)
        els_min = min([x for x in els if x != None])

        medial_pos = size / 2
        medial = els[medial_pos]
        left_seq = els[:medial_pos]
        right_seq = els[medial_pos + 1:]

        ## retain if medial is the first or last el
        if list(set(left_seq)) == [None] or list(set(right_seq)) == [None]:
            return medial
        ## repeations. Do not retain if medial is the second consecutive
        ## repeated cps
        elif medial == els[medial_pos - 1]:
            return None
        ## retain if medial is max or min
        elif medial == els_max or medial == els_min:
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
        cseg = Contour(el)
        all = set([tuple(x) for x in cseg.rotated_representatives()])
        r = 0
        # tests if an operation in cseg's all operation is already in
        # s set
        for op in all:
            if op in s:
                r += 1
        if r == 0:
            s.update([el])

    # sets the first contour of each class for function return
    result = []

    for el in s:
        cseg = Contour(el)
        all = [Contour(x) for x in cseg.rotated_representatives()]
        result.append(sorted(all)[0])

    return sorted(result)


class Contour(list):
    """Returns an object contour.
    Input is a list of cpitches:

    >>> Contour([0, 1, 3, 2])
    < 0 1 3 2 >
    """

    def rotation(self, factor=1):
        """Rotates a cseg around a factor.

        factor is optional. Default factor=1.

        'n' is the module of input factor. It's allowed to use factor
        numbers greater than cseg size.

        >>> Contour([0, 1, 2, 3]).rotation(2)
        < 2 3 0 1 >
        """

        n = factor % len(self)
        subset = self[n:]
        subset.extend(self[0:n])
        return Contour(subset)

    def retrogression(self):
        """Returns contour retrograde.

        >>> Contour([0, 1, 2, 3]).retrogression()
        < 3 2 1 0 >
        """

        return Contour(self[::-1])

    def inversion(self):
        """Returns contour inversion.

        >>> Contour([0, 3, 1, 2]).inversion()
        < 3 0 2 1 >
        """

        return Contour([(max(self) - cps) for cps in self])

    def translation(self):
        """Returns the normal form (Marvin 1987) of a given contour.
        It's the same of Friedmann (1985, 1987) contour class (CC).

        >>> Contour([4, 2, 6, 1]).translation()
        < 2 1 3 0 >
        """

        return Contour([sorted(set(self)).index(x) for x in self])

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

        for position in range(len(self) / 2):
            if self[position] != self[(position * -1) - 1]:
                return position

    def __prime_form_marvin_laprade_step_2(self, position):
        """Runs Marvin and Laprade (1987) second step of prime form
        algorithm.

        If (n - 1) - last pitch < first pitch, invert.

        position: the first cps position that its value is different
        for its symmetric (cf. unequal_edges).
        """

        cseg = self
        n = len(cseg)

        # if first and last cps are equal, the second must be compared
        # to penultimate cps and so on to break the "tie".
        false_first = cseg[position]
        false_last = cseg[(position * -1) - 1]

        if ((n - 1) - false_last) < false_first:
            cseg = cseg.inversion()

        return cseg

    def __prime_form_marvin_laprade_step_3(self, position):
        """Runs Marvin and Laprade (1987) third step of prime form
        algorithm.

        If last cpitch < first cpitch, retrograde.

        position: the first cps position that its value is different
        for its symmetric (cf. unequal_edges).
        """

        cseg = self

        if cseg[(position * -1) - 1] < cseg[position]:
            cseg = cseg.retrogression()

        return cseg

    def __non_repeated_prime_form_marvin_laprade(self):
        """Returns the prime form of a given contour (Marvin and
        Laprade, 1987)."""

        # the first cps position that its value is different for its
        # symmetric (cf. unequal_edges).
        position = self.__unequal_edges()

        # step 1: translate if necessary
        step1 = Contour(self).translation()
        step2 = step1.__prime_form_marvin_laprade_step_2(position)
        step3 = step2.__prime_form_marvin_laprade_step_3(position)

        return step3

    def __repeated_prime_generic(self, prime_algorithm):
        """Returns prime forms of a repeated cpitch cseg calculated
        with a given prime_algorithm.
        """

        triangle = self.comparison_matrix().superior_triangle()
        csegs = matrix.triangle_zero_replace_to_cseg(triangle)

        return sorted([auxiliary.apply_fn(t, prime_algorithm) for t in csegs])

    def __repeated_prime_form_marvin_laprade(self):
        """Returns prime forms of a repeated cpitch cseg."""

        return self.__repeated_prime_generic("prime_form_marvin_laprade")

    def prime_form_marvin_laprade(self):
        """Returns the prime form of a given contour (Marvin and
        Laprade, 1987).

        >>> Contour([4, 2, 6, 1]).prime_form_marvin_laprade()
        < 0 3 1 2 >
        """

        # tests if cseg has repeated elements
        if len(self) == len(set([x for x in self])):
            return self.__non_repeated_prime_form_marvin_laprade()
        else:
            return self.__repeated_prime_form_marvin_laprade()

    def __non_repeated_prime_form_sampaio(self):
        """Returns Sampaio prime form algorithm for non repeated
        c-pitches csegs.

        The Sampaio prime form algorithm returns the csegclass
        representative with the best ascendent numeric order.
        """
        return sorted(self.class_four_forms())[0]

    def __repeated_prime_form_sampaio(self):
        """Returns Sampaio prime form algorithm for repeated c-pitches
        csegs.

        Returns all possible prime forms of a cseg with repeated
        elements."""

        return self.__repeated_prime_generic("prime_form_sampaio")

    def prime_form_sampaio(self):
        """Runs Sampaio prime form algorithm.

        The Sampaio prime form algorithm returns the csegclass
        representative with the best ascendent numeric order.

        >>> Contour([0, 2, 1, 3, 4]).prime_form_sampaio()
        < 0 1 3 2 4 >
        """

        # tests if cseg has repeated elements
        if len(self) == len(set([x for x in self])):
            return self.__non_repeated_prime_form_sampaio()
        else:
            return self.__repeated_prime_form_sampaio()

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

        n_combinations = itertools.combinations(self, n)

        return sorted([Contour(list(x)) for x in n_combinations])

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
            processed = tuple(x.translation())
            if processed in dic:
                z = dic[processed]
                z.append(x)
                dic[processed] = z
            else:
                dic[processed] = [x]

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

        for x in subsets:
            processed = tuple(auxiliary.apply_fn(Contour(x), prime_algorithm))
            if processed in dic:
                z = dic[processed]
                z.append(x)
                dic[processed] = z
            else:
                dic[processed] = [x]

        return dic

    def all_subsets(self):
        """Returns adjacent and non-adjacent subsets of a given
        contour.

        >>> Contour([0, 1, 2]).all_subsets()
        [< 0 1 >, < 0 2 >, < 1 2 >, < 0 1 2 >]
        """

        sizes = range(2, len(self) + 1)
        return utils.flatten([self.subsets(x) for x in sizes])

    def all_subsets_prime(self, prime_algorithm="prime_form_sampaio"):
        """Returns all adjacent and non-adjacent subsets of a given
        contour grouped by their prime forms.

        >>> Contour([0, 1, 2]).all_subsets_prime()
        {(0, 1): [< 0 1 >, < 0 2 >, < 1 2 >], (0, 1, 2): [< 0 1 2 >]}
        """

        sizes = range(2, len(self) + 1)
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

        sizes = range(2, len(self) + 1)
        subsets_list = [self.subsets_normal(x) for x in sizes]
        [subsets_list[0].update(dic) for dic in subsets_list]
        return subsets_list[0]

    def subsets_adj(self, n):
        """Returns adjacent n-elements subsets of a given contour.

        >>> Contour([0, 1, 3, 2]).subsets_adj()
        [< 0 1 3 >, < 1 3 2 >]
        """

        return [Contour(self[i:i + n]) for i in range(len(self) - (n - 1))]

    def cps_position(self):
        """Returns a tuple with c-pitch and its position for each
        c-pitch of a cseg done.

        >>> Contour([0, 1, 3, 2]).cps_position()
        [(0, 0), (1, 1), (3, 2), (2, 3)]
        """

        return [(self[p], p) for p in range(len(self))]

    def reduction_morris(self):
        """Returns Morris (1993) contour reduction from a cseg, and
        its depth.

        >>> Contour([0, 4, 3, 2, 5, 5, 1]).reduction_morris()
        [< 0 2 1 >, 2]
        """

        def cps_position_to_cseg(cps_position):
            """Converts a list of cps_position tuples to cseg object."""

            return Contour([x for (x, y) in cps_position])

        def init_flag(tuples_list):
            """Returns max_list, min_list, flagged and unflagged
            cpitch tuples.

            Accepts a tuples_list with the original contour.

            It runs steps 1 and 2."""

            max_list = maxima_pair(tuples_list)
            min_list = minima_pair(tuples_list)

            # flagged cpitches are all cpitches that are in max_list
            # or min_list
            flagged = list(set(utils.flatten([max_list, min_list])))

            not_flagged = []
            for el in tuples_list:
                if el not in flagged:
                    not_flagged.append(el)

            return max_list, min_list, flagged, not_flagged

        def flag(max_list, min_list):
            """Returns max_list, min_list and unflagged cpitch tuples.

            It runs steps 6, and 7."""

            init_list = list(set(utils.flatten([max_list, min_list])))
            new_max_list = utils.remove_duplicate_tuples(maxima_pair(max_list))
            new_min_list = utils.remove_duplicate_tuples(minima_pair(min_list))

            # flagged cpitches are all cpitches that are in max_list
            # or min_list
            flagged = list(set(utils.flatten([new_max_list, new_min_list])))
            flagged = sorted(flagged, key=lambda(x, y): y)
            not_flagged = []
            # fills not_flagged:
            for el in init_list:
                if el not in flagged:
                    not_flagged.append(el)

            return new_max_list, new_min_list, flagged, not_flagged

        # returns list of cpitch/position tuples
        cseg_pos_tuples = self.cps_position()

        # initial value (step 0)
        depth = 0

        # runs steps 1 and 2
        max_list, min_list, flagged, not_flagged = init_flag(cseg_pos_tuples)

        if not_flagged != []:

            # step 5 (first time)
            depth += 1

            # loop to run unflagged until finish unflagged cpitches
            # tests if there are unflagged cpitches (partial step 3)
            while flag(max_list, min_list)[3] != []:
                # back to steps 6 and 7
                r = flag(max_list, min_list)
                max_list, min_list, flagged, not_flagged = r

                # increases depth (step 5)
                depth += 1

        sorted_flagged = sorted(flagged, key=lambda x: x[1])
        reduced = Contour(cps_position_to_cseg(sorted_flagged).translation())

        return [reduced, depth]

    def reduction_window(self, window_size=3, translation=True):
        """Returns a reduction in a single turn of n-window reduction
        algorithm. (Bor, 2009).

        >>> Contour([7, 10, 9, 0, 2, 3, 1, 8, 6, 2, 4, 5]).reduction_window(3, False)
        < 7 10 0 3 1 8 2 5>
        """

        def _red(cseg, pos, n):
            return reduction_retention(cseg[pos - n:pos + 1 + n])

        if window_size % 2 == 0:
            print "Window size must be an even number."
        else:
            cseg = self[:]
            size = len(cseg)
            n = window_size / 2

            for i in range(n):
                cseg.insert(0, None)
                cseg.append(None)

            prange = range(n, size + n)

            reduced = Contour([_red(cseg, pos, n) for pos in prange if _red(cseg, pos, n) != None])
            if translation == True:
                reduced = reduced.translation()
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

        cseg = self
        win_vals = [int(x) for x in str(windows)]
        for window in win_vals:
            cseg = cseg.reduction_window(window, translation)
        return [cseg, len(win_vals)]

    def reduction_sampaio(self, windows=3, translation=True):
        """Returns reduction contour and its depth with given windows
        sequence. (Sampaio, ?)
        """

        reduced, depth = self.reduction_bor(windows, translation)
        if self == reduced: depth = 0
        seq = reduced[:]
        i = 2

        while i < len(seq) - 1:
            if seq[i] == seq[i - 2] and seq[i + 1] == seq[i - 1]:
                seq.pop(i)
                seq.pop(i)
            else:
                i += 1

        seq = Contour(seq)
        if translation == True:
            seq = seq.translation()

        return [seq, depth + 1]

    def interval_succession(self):
        """Return Friedmann (1985) CIS, a series which indicates the
        order of Contour Intervals in a given CC (normal form cseg
        here).

        >>> Contour([1, 2, 3, 5, 4, 0]).interval_succession()
        [1, 1, 2, -1, -4]
        """

        return [b - a for a, b in zip(self, self[1:])]

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

        size = float(len(self))
        return self.absolute_intervals_sum() / size

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

        return self.absolute_intervals_sum() / float(highest(self))

    def internal_diagonals(self, n=1):
        """Returns Morris (1987) int_n. The first internal diagonal
        (int_1) is the same of Friedmann (1985, 1987) contour
        adjacency series (CAS).

        >>> Contour([0, 1, 3, 2]).internal_diagonals()
        < + + - >
        """

        matrix = self.comparison_matrix()
        int_d = [x for x in itertools.imap(cmp, matrix, itertools.islice(matrix, n, None)) if x != 0]
        return diagonal.InternalDiagonal(int_d)

    def comparison_matrix(self):
        """Returns Morris (1987) a cseg COM-Matrix.

        >>> Contour([0, 1, 3, 2]).comparison_matrix()
        0 + + +
        - 0 + +
        - - 0 -
        - - + 0
        """

        return matrix.ComparisonMatrix([[cmp(b, a) for b in self] for a in self])

    def fuzzy_membership_matrix(self):
        """Returns a Fuzzy membership matrix. Quinn (1997).

        >>> Contour([0, 1, 3, 2]).fuzzy_membership_matrix()
        0 1 1 1
        0 0 1 1
        0 0 0 0
        0 0 1 0
        """

        return fuzzy.FuzzyMatrix([[fuzzy.membership([a, b]) for b in self] for a in self])

    def fuzzy_comparison_matrix(self):
        """Returns a Fuzzy comparison matrix. Quinn (1997).

        >>> Contour([0, 1, 3, 2]).fuzzy_comparison_matrix()
        0 1 1 1
        -1 0 1 1
        -1 -1 0 -1
        -1 -1 1 0
        """

        return fuzzy.FuzzyMatrix([[fuzzy.comparison([a, b]) for b in self] for a in self])

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

        up_intervals = range(1, len(self))
        down_intervals = [-x for x in up_intervals]
        ups_list = []
        downs_list = []

        for x in itertools.combinations(self, 2):
            y = auxiliary.interval(x)
            if y > 0:
                ups_list.append(y)
            elif y < 0:
                downs_list.append(y)

        ups = [ups_list.count(x) for x in up_intervals]
        downs = [downs_list.count(x) for x in down_intervals]

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

        items = range(1, len(self))
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

        return [sum(x) for x in self.interval_array()]

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
            return float(ups) / total
        else:
            return float(downs) * -1 / total

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
        cseg_classes = utils.flatten(build_classes(len(self), prime_algorithm))
        for (cardinality, number, cseg_class, ri_identity) in cseg_classes:
            if tuple(prime_form) == cseg_class:
                r = cardinality, number, Contour(list(cseg_class)), ri_identity
                return r

    def ri_identity_test(self):
        """Returns True if cseg have identity under retrograded
        inversion.

        >>> Contour([0, 1, 3, 2]).ri_identity_test()
        False
        """

        i = Contour(self).inversion()
        ri = Contour(i).retrogression()
        return self == ri

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

        cseg = self
        ri = self.retrogression().inversion()
        size_half = round(len(cseg) / 2.0)
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

        p = auxiliary.apply_fn(Contour(self), prime_algorithm)
        i = Contour(self).inversion()
        r = Contour(self).retrogression()
        ri = Contour(i).retrogression()

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

        size = len(self)
        return [self.rotation(n) for n in range(size + 1)]

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
        result = set([tuple(x) for x in result])

        return sorted([Contour(list(x)) for x in list(result)])

    def base_three_representation(self):
        """Returns Base three Contour Description, by Polansky and
        Bassein (1992). The comparison between c-points returns 0, 1,
        or 2 if the second c-point is lower, equal or higher than the
        first, respectively. This method returns a list with
        comparison of all combinations of c-points.

        >>> Contour([0, 1, 3, 2]).base_three_representation()
        [[2, 2, 2], [2, 2], [0]]
        """

        combinations = itertools.combinations(self, 2)

        def aux_list(base_3, self):
            size = len(self)
            r_size = range(size - 1, 0, -1)
            result = []
            n = 0
            for i in r_size:
                seq = base_3[n:n + i]
                result.append(seq)
                n += i
            return result

        ternary = [auxiliary.base_3_comparison(a, b) for a, b in combinations]

        return aux_list(ternary, self)

    def oscilation(self):
        """Returns number of direction changes of a given
        cseg. (Schmuckler, 1999).
        """

        int_1 = self.internal_diagonals()
        return sum([1 for i in range(len(int_1) - 1) if int_1[i] != int_1[i + 1]])

    def oscilation_index(self):
        """Returns index of direction changes of a given
        cseg. (Schmuckler, 1999).
        """

        return self.oscilation() / float(len(self) - 1)

    def __repr__(self):
        return "< {0} >".format(" ".join([str(x) for x in self[:]]))


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
        if cseg.unique_prime_form_test(prime_form_algorithm) == False:
            c_class, n_class, x, ri = cseg.segment_class()
            coll.add((c_class, n_class))

    classes = sorted(list(coll))
    result = []

    if classes != []:
        for cls in classes:
            cseg = auxiliary.cseg_from_class_number(*cls)
            ri = cseg.retrogression().inversion()
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
