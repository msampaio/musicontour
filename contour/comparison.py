#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import itertools
import numpy
import contour
from contour import Contour
import __utils as utils
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

    return utils.position_comparison(cseg1_triangle, cseg2_triangle)


def csegclass_similarity(cseg1, cseg2, prime_algorithm="prime_form_marvin_laprade"):
    """Returns Marvin and Laprade (1987) CSIM(_A, _B) with csegclasses
    representatives comparison.

    >>> csegclass_similarity(Contour([0, 2, 3, 1]), Contour([3, 1, 0, 2]))
    1
    """

    cseg1_p = utils.apply_fn(cseg1, prime_algorithm)
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


def cseg_mutually_embedded(n, obj_cseg1, obj_cseg2):
    """Returns CMEMBn(X, A, B) (Marvin and Laprade, 1987) auxiliary
    values.

    >>> mutually_embed_cseg(Contour([0, 1, 2]), Contour([0, 1, 3, 2]))
    4
    """

    subsets1 = obj_cseg1.subsets_normal(n)
    subsets2 = obj_cseg2.subsets_normal(n)
    common_csegs = set(subsets2.keys()) & set(subsets1.keys())

    n = 0
    for key in common_csegs:
        for obj_cseg in subsets1[key]:
            n += utils.count_sets(obj_cseg.cseg, obj_cseg1.cseg)
        for obj_cseg in subsets2[key]:
            n += utils.count_sets(obj_cseg.cseg, obj_cseg2.cseg)
    return n


def all_cseg_mutually_embedded(obj_cseg1, obj_cseg2):
    """Returns ACMEMB(A, B) (Marvin and Laprade, 1987) values.

    >>> all_cseg_mutually_embedded(Contour([0, 1, 2, 3]), Contour([0, 2, 1, 3, 4]))
    0.7837837837837838
    """

    card1 = obj_cseg1.size
    card2 = obj_cseg2.size

    cards = range(2, max([card1, card2]) + 1)
    n = sum([cseg_mutually_embedded(n, obj_cseg1, obj_cseg2) for n in cards])
    return n / float(utils.number_of_possible_mutually_subsets(card1, card2))


def cseg_similarity_continuum(obj_cseg, prime_algorithm="prime_form_marvin_laprade"):
    """Returns all csegs with the same cardinality of the given one
    sorted by cseg similarity.

    >>> cseg_similarity_continuum(Contour([1, 0, 3, 2]))
    [[0.5, [< 0 2 1 3 >, < 0 3 2 1 >]],
     [0.66666666666666663, [< 0 1 2 3 >, < 0 2 3 1 >, < 0 3 1 2 >]],
     [0.83333333333333337, [< 0 1 3 2 >, < 1 3 0 2 >]],
     [1.0, [< 1 0 3 2 >]]]
    """

    all_csegs = [Contour(el) for el in utils.permut_csegs(obj_cseg.size)]

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
        acmemb = all_cseg_mutually_embedded(cseg, prime)
        result.append([prime, acmemb])

    return sorted(result, key=lambda x: x[1])

# fuzzy operations
def entry_numbers(size):
    """Returns the entries to be compared in a fuzzy comparison
    matrix. Quinn 1997, equation 6.2.

    >>> entry_numbers(5)
    20
    """

    return (size ** 2) - size


def entry_numbers_cseg(cseg):
    """Returns the entries to be compared in a fuzzy comparison
    matrix. Quinn 1997, equation 6.2.

    >>> entry_numbers_cseg(Contour([2, 0, 3, 1, 4]))
    20
    """

    return entry_numbers(len(cseg))


def similarity_increment(el_1, el_2, entries_number):
    """Returns increment for fuzzy retrofitting similarity comparison
    function. Quinn 1997, equation 6.4.

    el_1 = fuzzy comparison matrix entry for cseg 1
    el_2 = fuzzy comparison matrix entry for cseg 2

    >>> similarity_increment(0.8, 0.9, 2)
    0.45
    """

    return (1 - abs(el_2 - el_1)) / float(entries_number)


def fuzzy_similarity_matrix(matrix1, matrix2):
    """Returns fuzzy ascent membership similarity between two ascend
    matrices. Quinn 1997, based on figure 11.

    >>> matrix_similarity_fuzzy([[0, 0.8], [0, 0]], [[0, 0.9], [0, 0]])
    0.95
    """

    size = len(matrix1[0])
    rsize = range(size)

    # number of compared entries
    j = entry_numbers(size)

    # fuzzy comparison matrix without zero main diagonal
    m1 = numpy.matrix(matrix1)
    m2 = numpy.matrix(matrix2)

    def __increment(m1, m2, j, x, y):
        return (1 - abs(m1.item(x, y) - m2.item(x, y))) / float(j)

    matrix_model = [(x, y) for x, y in itertools.product(rsize, rsize) if x != y]

    return sum([__increment(m1, m2, j, x, y) for x, y in matrix_model])


def fuzzy_similarity(cseg1, cseg2):
    """Returns fuzzy ascent membership similarity between two csegs.
    Quinn 1997, figure 11.

    >>> similarity_fuzzy(Contour([4, 1, 2, 3, 0]), Contour([4, 0, 1, 3, 2]))
    0.8
    """

    m1 = cseg1.fuzzy_membership_matrix()
    m2 = cseg2.fuzzy_membership_matrix()
    return fuzzy_similarity_matrix(m1, m2)

