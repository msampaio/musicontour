#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from contour import Contour
from math import factorial


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


def subsets_embed_total_number(cseg_size, csubseg_size):
    """Returns the number of subsets with csubseg_size in a set with
    cseg_size. Marvin and Laprade (1987, p. 237)."""

    try:
        cseg_size >= csubseg_size == True
        a = factorial(cseg_size)
        b = factorial(csubseg_size)
        c = factorial(cseg_size - csubseg_size)
        return a / (b * c)
    # FIXME: use ContourError
    except ValueError:
        print("Cseg_size must be greater than csubseg_size")


def subsets_embed_number(cseg, csubseg):
    """Returns the number of time the normal form of a csubseg appears
    in cseg subsets. Marvin and Laprade (1987)."""

    try:
        dic = Contour(cseg).subsets_normal(len(csubseg))
        return len(dic[tuple(csubseg)])

    except ValueError:
        print("Cseg must be greater than csubseg.")


def contour_embed(cseg1, cseg2):
    """Returns similarity between contours with different
    cardinalities. 1 for greater similarity. Marvin and Laprade
    (1987)."""

    if cseg1 > cseg2:
        cseg = cseg1
        csubseg = cseg2
    else:
        cseg = cseg2
        csubseg = cseg1

    n_csubseg = Contour(csubseg).translation()
    cseg_size = len(cseg)
    csubseg_size = len(csubseg)

    embed_times = subsets_embed_number(cseg, n_csubseg)
    total_subsets = subsets_embed_total_number(cseg_size, csubseg_size)
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
        cseg1_s = Contour(cseg1).subsets_normal(cardinality)
        cseg2_s = Contour(cseg2).subsets_normal(cardinality)
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
