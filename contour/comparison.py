#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import contour
from contour import Contour
import utils
import auxiliary
from collections import Counter

def cseg_similarity(cseg1, cseg2):
    """Returns Marvin and Laprade (1987) CSIM(A, B) for a single
    cseg. It's a contour similarity function that measures similarity
    between two csegs of the same cardinality. The maximum similarity
    is 1, and minimum is 0.

    >>> cseg_similarity(Contour([0, 2, 3, 1]), Contour([3, 1, 0, 2]))
    0
    """

    cseg1_triangle = utils.flatten(cseg1.comparison_matrix().superior_triangle())
    cseg2_triangle = utils.flatten(cseg2.comparison_matrix().superior_triangle())

    return auxiliary.position_comparison(cseg1_triangle, cseg2_triangle)


def csegclass_similarity(cseg1, cseg2, prime_algorithm="prime_form_marvin_laprade"):
    """Returns Marvin and Laprade (1987) CSIM(_A, _B) with csegclasses
    representatives comparison.

    >>> csegclass_similarity(Contour([0, 2, 3, 1]), Contour([3, 1, 0, 2]))
    1
    """

    cseg1_p = auxiliary.apply_fn(cseg1, prime_algorithm)
    representatives = cseg2.class_representatives()
    csims = [cseg_similarity(cseg1_p, c) for c in representatives]
    return sorted(csims, reverse=True)[0]


# FIXME: review function to use: cseg_similarity or csegclass_similarity
def cseg_similarity_matrix(csegs):
    """Returns a matrix with CSIM between multiple csegs.

    >>> cseg_similarity_matrix([Contour([0, 1, 2, 3]), Contour([1, 0, 3, 2])])
    [[< 0 1 2 3 >, < 1 0 3 2 >],
    [1.0, 0.66666666666666663],
    [0.66666666666666663, 1.0]]
    """

    m = []
    for a in csegs:
        line = []
        for b in csegs:
            line.append(csegclass_similarity(a, b))
        m.append(line)
    m.insert(0, csegs)
    return m


def cseg_similarity_matrix_classes(card, prime_algorithm="prime_form_sampaio"):
    """Returns a matrix with CSIM between multiple csegs.

    >>> cseg_similarity_matrix_classes(3)
    [[< 0 1 2 >, < 0 2 1 >],
    [1.0, 0.66666666666666663],
    [0.66666666666666663, 1.0]]
    """

    classes_lst = contour.build_classes_card(card, prime_algorithm)
    classes = [Contour(cseg) for (a, b, cseg, c) in classes_lst]

    return cseg_similarity_matrix(classes)


def subsets_embedded_total_number(cseg1, cseg2):
    """Returns the number of subsets with csubseg_size in a set with
    cseg_size. Marvin and Laprade (1987, p. 237).

    >>> c1, c2 = Contour([0, 1, 2, 3]), Contour([1, 0, 2])
    >>> subsets_embedded_total_number(c1, c2)
    4
    """

    cseg, csubseg = utils.greatest_first(cseg1, cseg2)
    cseg_size = len(cseg)
    csubseg_size = len(csubseg)

    a = math.factorial(cseg_size)
    b = math.factorial(csubseg_size)
    c = math.factorial(cseg_size - csubseg_size)
    return a / (b * c)


def subsets_embedded_number(cseg1, cseg2):
    """Returns the number of time the normal form of a csubseg appears
    in cseg subsets. Marvin and Laprade (1987).

    >>> c1, c2 = Contour([0, 1, 2, 3]), Contour([1, 0, 2])
    >>> subsets_embedded_number(c1, c2)
    0
    """

    cseg, csubseg = utils.greatest_first(cseg1, cseg2)

    dic = Contour(cseg).subsets_normal(len(csubseg))
    tup = tuple(csubseg.cseg)
    if tup in dic:
        return len(dic[tup])
    else:
        return 0


def contour_embedded(cseg1, cseg2):
    """Returns similarity between contours with different
    cardinalities. 1 for greater similarity. (CEMB(a,b)). Marvin and
    Laprade (1987).

    >>> contour_embedded(Contour([0, 1, 2, 3]), Contour([0, 1, 2]))
    1.0
    """

    cseg, csubseg = utils.greatest_first(cseg1, cseg2)

    n_csubseg = Contour(csubseg).translation()
    cseg_size = len(cseg)
    csubseg_size = len(csubseg)

    embedded_times = subsets_embedded_number(cseg, n_csubseg)
    total_subsets = subsets_embedded_total_number(cseg, csubseg)
    return float(embedded_times) / total_subsets


def cseg_similarity_compare(cseg1, cseg2):
    """Returns Cseg Embedded if cseg have different cardinality, and Cseg
    Similarity, if csegs have the same similarity.

    >>> cseg_similarity_compare(Contour([0, 1, 2, 3]), Contour([0, 1, 2]))
    ['cseg embedded', 1.0]
    """

    if len(cseg1) != len(cseg2):
        return ["Cseg embedded", contour_embedded(cseg1, cseg2)]
    else:
        return ["Cseg similarity", cseg_similarity(cseg1, cseg2)]


def __csubseg_mutually_embedded(cardinality, cseg1, cseg2):
    """Returns CMEMBn(X, A, B) (Marvin and Laprade, 1987) auxiliary
    values.

    Outputs a list with [incidence_number, total_numbers]

    All subsets of a given cardinality (n) are counted if they are
    embedded in both csegs A and B. This number is divided by the sum of
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
    normal form embedded in cseg1 and cseg2.

    >>> __csubseg_mutually_embedded(3, Contour([0, 1, 2, 3]), Contour([0, 1, 2]))
    [5, 5]
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


def csubseg_mutually_embedded(cardinality, cseg1, cseg2):
    """Returns CMEMBn(X, A, B) (Marvin and Laprade, 1987).

    >>> csubseg_mutually_embedded(3, Contour([0, 1, 2, 3]), Contour([0, 1, 2]))
    1.0
    """

    [a, b] = __csubseg_mutually_embedded(cardinality, cseg1, cseg2)
    return float(a) / b


def __all_contour_mutually_embedded(cseg1, cseg2):
    """Returns ACMEMB(A,B) (Marvin and Laprade, 1987).

    It's total number of significant mutually embeddeded csegs of
    cardinality 2 through the cardinality of the smaller cseg divided
    by the total possible csegs embedded in both cseg1 and cseg2.

    >>> __all_contour_mutually_embedded(Contour([0, 1, 2, 3]), Contour([0, 1, 2]))
    0.93333333333333335
    """

    incidence, total = (0, 0)
    for i in range(2, max(len(cseg1), len(cseg2)) + 1):
        incidence += __csubseg_mutually_embedded(i, cseg1, cseg2)[0]
        total += __csubseg_mutually_embedded(i, cseg1, cseg2)[1]
    return float(incidence) / total


def all_contour_mutually_embedded(cseg1, cseg2):
    """Returns ACMEMB(A,B) (Marvin and Laprade, 1987).

    It's total number of significant mutually embeddeded csegs of
    cardinality 2 through the cardinality of the smaller cseg divided
    by the total possible csegs embedded in both cseg1 and cseg2 and its
    csegclasses representatives.

    >>> all_contour_mutually_embedded(Contour([0, 1, 2, 3]), Contour([0, 1, 2]))
    0.93333333333333335
    """

    four_forms = cseg2.class_four_forms()
    acmembs = [__all_contour_mutually_embedded(cseg1, c) for c in four_forms]
    return sorted(acmembs, reverse=True)[0]


def cseg_similarity_continuum(obj_cseg, prime_algorithm="prime_form_marvin_laprade"):
    """Returns all csegs with the same cardinality of the given one
    sorted by cseg similarity.

    >>> cseg_similarity_continuum(Contour([1, 0, 3, 2]))
    [[0.5, [< 0 2 1 3 >, < 0 3 2 1 >]],
     [0.66666666666666663, [< 0 1 2 3 >, < 0 2 3 1 >, < 0 3 1 2 >]],
     [0.83333333333333337, [< 0 1 3 2 >, < 1 3 0 2 >]],
     [1.0, [< 1 0 3 2 >]]]
    """

    all_csegs = [Contour(el) for el in auxiliary.permut_csegs(obj_cseg.size)]

    dic = Counter()
    for cseg_ob in all_csegs:
        csim = cseg_similarity(obj_cseg, cseg_ob)
        if csim not in dic:
            dic[csim] = []
        dic[csim].append(cseg_ob)
    return [[k, dic[k]] for k in sorted(dic)]


def cseg_similarity_subsets_continuum(cseg, prime_algorithm="prime_form_sampaio"):
    """Returns all csegs with smaller cardinality of the given one
    sorted by cseg similarity.

    >>> cseg_similarity_subsets_continuum(Contour([0, 1, 2, 3]))
    [[< 0 1 >, 0.58333333333333337],
    [< 0 1 2 >, 0.93333333333333335],
    [< 0 1 2 3 >, 1.0]]
    """

    subsets = cseg.all_subsets_prime().keys()

    result = []

    for subset in subsets:
        prime = Contour(subset)
        acmemb = all_contour_mutually_embedded(cseg, prime)
        result.append([prime, acmemb])

    return sorted(result, key=lambda x: x[1])
