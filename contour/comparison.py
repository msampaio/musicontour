#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import math
import contour
import utils


def __intern_diagon_sim(cseg1, cseg2, n):
    """Returns the number of positions where cseg1 and cseg2 have the
    same value in a n-internal diagonal."""

    c1, c2 = contour.Contour(cseg1), contour.Contour(cseg2)
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


def subsets_embed_total_number(cseg1, cseg2):
    """Returns the number of subsets with csubseg_size in a set with
    cseg_size. Marvin and Laprade (1987, p. 237)."""

    cseg, csubseg = utils.greatest_first(cseg1, cseg2)
    cseg_size = len(cseg)
    csubseg_size = len(csubseg)

    a = math.factorial(cseg_size)
    b = math.factorial(csubseg_size)
    c = math.factorial(cseg_size - csubseg_size)
    return a / (b * c)


def subsets_embed_number(cseg1, cseg2):
    """Returns the number of time the normal form of a csubseg appears
    in cseg subsets. Marvin and Laprade (1987)."""

    cseg, csubseg = utils.greatest_first(cseg1, cseg2)

    dic = contour.Contour(cseg).subsets_normal(len(csubseg))
    if tuple(csubseg) in dic:
        return len(dic[tuple(csubseg)])
    else:
        return 0


def contour_embed(cseg1, cseg2):
    """Returns similarity between contours with different
    cardinalities. 1 for greater similarity. Marvin and Laprade
    (1987)."""

    cseg, csubseg = utils.greatest_first(cseg1, cseg2)

    n_csubseg = contour.Contour(csubseg).translation()
    cseg_size = len(cseg)
    csubseg_size = len(csubseg)

    embed_times = subsets_embed_number(cseg, n_csubseg)
    total_subsets = subsets_embed_total_number(cseg, csubseg)
    return 1.0 * embed_times / total_subsets


def cseg_similarity_compare(cseg1, cseg2):
    """Returns Cseg Embed if cseg have different cardinality, and Cseg
    Similarity, if csegs have the same similarity.

    Output example: [\"cseg embed\", 1]
    """

    if len(cseg1) != len(cseg2):
        return ["Cseg embed", contour_embed(cseg1, cseg2)]
    else:
        return ["Cseg similarity", cseg_similarity(cseg1, cseg2)]


def __csubseg_mutually_embed(cardinality, cseg1, cseg2):
    """Returns CMEMBn(X, A, B) (Marvin and Laprade, 1987) auxiliary
    values.

    Outputs a list with [incidence_number, total_numbers]

    All subsets of a given cardinality (n) are counted if they are
    embed in both csegs A and B. This number is divided by the sum of
    total contour subsets number of that cardinality in each segment,
    A, and B.

    'cseg1_s' and 'cseg2_s' store dictionaries with all their subsegs
    and related normal forms.

    'cseg1_t' and 'cseg2_t' store the number of csubsegs related to
    each normal form.

    'total_number' store the sum of all possible subsets of same
    cardinality for each contour cseg1, and cseg2.

    'intersection' store a list with normal forms common to cseg1 and
    cseg2.

    'incidence_number' stores the sum of subsets related by the same
    normal form embed in cseg1 and cseg2.
    """

    try:
        cseg1_s = contour.Contour(cseg1).subsets_normal(cardinality)
        cseg2_s = contour.Contour(cseg2).subsets_normal(cardinality)
        cseg1_t = 0
        cseg2_t = 0

        for key in cseg1_s.keys():
            cseg1_t += len(cseg1_s[key])

        for key in cseg2_s.keys():
            cseg2_t += len(cseg2_s[key])

        total_number = cseg1_t + cseg2_t

        intersection = list(set(cseg2_s.keys()) & set(cseg1_s.keys()))
        incidence_number = 0

        for key in intersection:
            incidence_number += len(cseg1_s[key])
            incidence_number += len(cseg2_s[key])

        return [incidence_number, total_number]

    except ValueError:
        print("Csegs length must be greater than cardinality.")


def csubseg_mutually_embed(cardinality, cseg1, cseg2):
    """Returns CMEMBn(X, A, B) (Marvin and Laprade, 1987)."""

    [a, b] = __csubseg_mutually_embed(cardinality, cseg1, cseg2)
    return 1.0 * a / b


def all_contour_mutually_embed(cseg1, cseg2):
    """Returns ACMEMB(A,B) (Marvin and Laprade, 1987).

    It's total number of significant mutually embeded csegs of
    cardinality 2 through the cardinality of the smaller cseg divided
    by the total possible csegs embed in both cseg1 and cseg2.
    """

    incidence, total = (0, 0)
    for i in range(2, max(len(cseg1), len(cseg2)) + 1):
        incidence += __csubseg_mutually_embed(i, cseg1, cseg2)[0]
        total += __csubseg_mutually_embed(i, cseg1, cseg2)[1]
    return 1.0 * incidence / total


def operations_comparison(*csegs):
    """Returns contour operations relations between each couple of
    csegs of a list."""

    def apply_fn(cseg, fn):
        return apply(getattr(contour.Contour(cseg), fn))

    def remove_operation_repetition(op_list):
        """Removes operations repetitions.
        For input l = [[a, b], [b, a], [c, d]], the output is
        [[a, b], [c, d]]

        >>> l = [[[(0, 1, 2), 'retrograde'], [(2, 1, 0), 'original']],
        [[(2, 1, 0), 'original'], [(0, 1, 2), 'retrograde']]]
        >>> remove_operation_repetition(l)
        [[(0, 1, 2), 'retrograde'], [(2, 1, 0), 'original']]"""

        new_list = []

        for i in op_list:
            if [i[1], i[0]] not in new_list:
                new_list.append(i)
        return new_list

    def find_relations(dictionary):
        relations = []
        for a in dictionary:
            for b in dictionary:
                if dictionary[a] == dictionary[b]:
                    (m, n) = a
                    (o, p) = b
                    if m != o:
                        relations.append([[contour.Contour(list(m)), n], [contour.Contour(list(o)), p]])
        return remove_operation_repetition(relations)

    def build_dictionary(csegs):
        cseg_op = {}
        for cseg in csegs:
            cseg_op[(tuple(cseg), 'original')] = cseg
            for fn in operations:
                normal_form = apply_fn(contour.Contour(cseg).translation(), fn)
                reduced = contour.Contour(cseg).reduction_algorithm()
                ## removes csegs that are equal to their normal form
                ## or reduced algorithm form
                if cseg != normal_form or cseg != reduced[0]:
                    cseg_op[(tuple(cseg), fn)] = normal_form
        return cseg_op

    operations = ["translation", "prime_form", "inversion", "retrograde", "reduction_algorithm", "rotation"]
    cseg_op = build_dictionary(csegs)

    return find_relations(cseg_op)

def pretty_operations_comparison(*csegs):
    """Prints a pretty result for operations comparison."""

    r = []
    for [[a, b], [c, d]] in operations_comparison(*csegs):
        r.append("{1}({0}) = {3}({2})".format(a, b, c, d))
    return "\n".join(r)
