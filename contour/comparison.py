#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import contour
import utils
import auxiliary


def __intern_diagon_sim(cseg1, cseg2, n):
    """Returns the number of positions where cseg1 and cseg2 have the
    same value in a n-internal diagonal."""

    c1, c2 = contour.Contour(cseg1), contour.Contour(cseg2)
    d1, d2 = c1.internal_diagonals(n), c2.internal_diagonals(n)
    length = len(d1)
    return sum([(1 if d1[i] == d2[i] else 0) for i in range(length)])


def single_cseg_similarity(cseg1, cseg2):
    """Returns Marvin and Laprade (1987) CSIM(A, B) for a single
    cseg. It's a contour similarity function that measures similarity
    between two csegs of the same cardinality. The maximum similarity
    is 1, and minimum is 0.

    'd' means the number of internal diagonals.

    'triang_pos' is the number of positions in triangle above the zero
    diagonal.

    'similar pos' is the number of positions where cseg1 and cseg2
    have the same value. This variable is calculated with the private
    method __intern_diagon_sim().

    >>> single_cseg_similarity(Contour([0, 2, 3, 1]), Contour([3, 1, 0, 2]))
    0
    """

    d = range(len(cseg1))
    d.remove(0)
    triangle_pos = sum(d)
    similar_pos = sum([__intern_diagon_sim(cseg1, cseg2, n) for n in d])
    return similar_pos / float(triangle_pos)


def cseg_similarity(cseg1, cseg2):
    """Returns Marvin and Laprade (1987) CSIM(A, B) with csegclasses
    representatives comparison.

    >>> cseg_similarity(Contour([0, 2, 3, 1]), Contour([3, 1, 0, 2]))
    1
    """

    representatives = cseg2.class_representatives()
    csims = [single_cseg_similarity(cseg1, c) for c in representatives]
    return sorted(csims, reverse=True)[0]


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
            line.append(cseg_similarity(a, b))
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
    classes = [contour.Contour(list(cseg)) for (a, b, cseg, c) in classes_lst]

    return cseg_similarity_matrix(classes)


def subsets_embed_total_number(cseg1, cseg2):
    """Returns the number of subsets with csubseg_size in a set with
    cseg_size. Marvin and Laprade (1987, p. 237).

    >>> c1, c2 = Contour([0, 1, 2, 3]), Contour([1, 0, 2])
    >>> subsets_embed_total_number(c1, c2)
    4
    """

    cseg, csubseg = utils.greatest_first(cseg1, cseg2)
    cseg_size = len(cseg)
    csubseg_size = len(csubseg)

    a = math.factorial(cseg_size)
    b = math.factorial(csubseg_size)
    c = math.factorial(cseg_size - csubseg_size)
    return a / (b * c)


def subsets_embed_number(cseg1, cseg2):
    """Returns the number of time the normal form of a csubseg appears
    in cseg subsets. Marvin and Laprade (1987).

    >>> c1, c2 = Contour([0, 1, 2, 3]), Contour([1, 0, 2])
    >>> subsets_embed_number(c1, c2)
    0
    """

    cseg, csubseg = utils.greatest_first(cseg1, cseg2)

    dic = contour.Contour(cseg).subsets_normal(len(csubseg))
    if tuple(csubseg) in dic:
        return len(dic[tuple(csubseg)])
    else:
        return 0


def contour_embed(cseg1, cseg2):
    """Returns similarity between contours with different
    cardinalities. 1 for greater similarity. Marvin and Laprade
    (1987).

    >>> contour_embed(Contour([0, 1, 2, 3]), Contour([0, 1, 2]))
    1.0
    """

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

    >>> cseg_similarity_compare(Contour([0, 1, 2, 3]), Contour([0, 1, 2]))
    ['cseg embed', 1.0]
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

    >>> __csubseg_mutually_embed(3, Contour([0, 1, 2, 3]), Contour([0, 1, 2]))
    [5, 5]
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
    """Returns CMEMBn(X, A, B) (Marvin and Laprade, 1987).

    >>> csubseg_mutually_embed(3, Contour([0, 1, 2, 3]), Contour([0, 1, 2]))
    1.0
    """

    [a, b] = __csubseg_mutually_embed(cardinality, cseg1, cseg2)
    return 1.0 * a / b


def __all_contour_mutually_embed(cseg1, cseg2):
    """Returns ACMEMB(A,B) (Marvin and Laprade, 1987).

    It's total number of significant mutually embeded csegs of
    cardinality 2 through the cardinality of the smaller cseg divided
    by the total possible csegs embed in both cseg1 and cseg2.

    >>> __all_contour_mutually_embed(Contour([0, 1, 2, 3]), Contour([0, 1, 2]))
    0.93333333333333335
    """

    incidence, total = (0, 0)
    for i in range(2, max(len(cseg1), len(cseg2)) + 1):
        incidence += __csubseg_mutually_embed(i, cseg1, cseg2)[0]
        total += __csubseg_mutually_embed(i, cseg1, cseg2)[1]
    return 1.0 * incidence / total


def all_contour_mutually_embed(cseg1, cseg2):
    """Returns ACMEMB(A,B) (Marvin and Laprade, 1987).

    It's total number of significant mutually embeded csegs of
    cardinality 2 through the cardinality of the smaller cseg divided
    by the total possible csegs embed in both cseg1 and cseg2 and its
    csegclasses representatives.

    >>> all_contour_mutually_embed(Contour([0, 1, 2, 3]), Contour([0, 1, 2]))
    0.93333333333333335
    """

    representatives = cseg2.class_representatives()
    acmembs = [__all_contour_mutually_embed(cseg1, c) for c in representatives]
    return sorted(acmembs, reverse=True)[0]


def operations_comparison(cseg1, cseg2, prime_algorithm="prime_form_marvin_laprade"):
    """Returns contour operations relations between two given csegs.

    >>> operations_comparison(Contour([0, 1, 2, 3]), Contour([3, 1, 2, 0]))
    [[(< 0 1 2 3 >, 2, 'internal_diagonals', < + - + >),
    (< 3 1 2 0 >, 1, 'internal_diagonals', < + - + >)]]
    """

    operations = ["translation", prime_algorithm, "inversion",
                  "retrograde", "reduction_morris", "internal_diagonals"]

    def all_rotations(cseg):
        """Returns all possible rotations of a given cseg.

        >>> all_rotations(Contour([0, 1, 2])
        [(< 0, 1, 2>, 0, < 0, 1, 2 >),
        (< 0, 1, 2 >, 1, < 1, 2, 0 >),
        (< 0, 1, 2 >, 2, < 2, 0, 1 >)]
        """

        s = len(cseg)
        return [(cseg, factor, cseg.rotation(factor)) for factor in range(s)]

    def all_op(cseg, factor, rotated):
        """Returns all operations defined in variable 'operations' of
        a given tuple (original cseg, rotation factor, and rotated
        cseg)."""

        def __append_op(lst, cseg, factor, op):
            """Appends cseg, factor, and operation data to a given
            list.
            """

            lst.append((cseg, factor, op, auxiliary.apply_fn(rotated, op)))

        r = []
        r.append((cseg, factor, "original", rotated))
        [__append_op(r, cseg, factor, op) for op in operations]

        return r

    def all_op_all_rot(cseg):
        """Returns a list with all operations of all rotations of a
        given cseg."""

        r = []
        for (c, factor, rotated) in all_rotations(cseg):
            r.append(all_op(c, factor, rotated))

        return utils.flatten(r)

    def compare_csegs(cseg1, cseg2, prime_algorithm):
        """Returns a list of operations that csegs are related. If
        csegs are related by original, prime or normal form, only the
        first relations is returned. The test order is 'original',
        'normal form', and 'prime form'."""

        l1 = all_op_all_rot(cseg1)
        l2 = all_op_all_rot(cseg2)

        r = []

        for x in l1:
            for y in l2:

                # Tests if csegs are related by basic operations
                if list(x)[3] == list(y)[3]:
                    if list(x)[2] == list(y)[2] == "original":
                        r = [[x, y]]
                        break

                    # Tests csegs with the same rotation factor.
                    elif list(x)[1] == list(y)[1] == 0:
                        if list(x)[2] == list(y)[2] == "translation":
                            r = [[x, y]]
                            break
                        elif list(x)[2] == list(y)[2] == prime_algorithm:
                            r = [[x, y]]
                            break
                    else:
                        r.append([x, y])

        # if csegs have different rotation factor, but are in prime
        # or normal form, break
        result = []
        for (x, y) in r:
            if list(x)[2] or list(y)[2] == prime_algorithm or "translation":
                result = [[x, y]]
                break
            else:
                result.append([x, y])

        return result

    return compare_csegs(cseg1, cseg2, prime_algorithm)


def pretty_operations_comparison(cseg1, cseg2, prime_algorithm="prime_form_marvin_laprade"):
    """Prints a pretty result for operations comparison.

    >>> c1, c2 = Contour([0, 1, 2, 3]), Contour([3, 1, 2, 0])
    >>> pretty_operations_comparison(c1, c2)
    '< 0 1 2 3 > [rot1] (internal_diagonals): < + - + >\n' +
    '< 3 1 2 0 > [rot1] (internal_diagonals)\n'
    """

    r = []
    op_data = operations_comparison(cseg1, cseg2, prime_algorithm)

    for [(c1, f1, o1, r1), (c2, f2, o2, r2)] in op_data:
        els = c1, f2, o1, r1, c2, f2, o2
        r.append("{0} [rot{1}] ({2}): {3}\n{4} [rot{5}] ({6})\n".format(*els))
    if r == []:
        return "No operation similarity."
    else:
        return "\n".join(r)


def cseg_similarity_continuum(cseg, prime_algorithm="prime_form_marvin_laprade"):
    """Returns all csegs with the same cardinality of the given one
    sorted by cseg similarity.

    >>> cseg_similarity_continuum(Contour([1, 0, 3, 2]))
    [[0.5, [< 0 2 1 3 >, < 0 3 2 1 >]],
    [0.66666666666666663, [< 0 1 2 3 >, < 0 2 3 1 >, < 0 3 1 2 >]],
    [0.83333333333333337, [< 0 1 3 2 >, < 1 3 0 2 >]],
    [1.0, [< 1 0 3 2 >]]]
    """

    size = len(cseg)
    built_classes = contour.build_classes_card(size, prime_algorithm)

    def cseg_similarity_lists(built_classes):
        """Returns a tuple with two lists:
        1. cseg similarity (CSIM) and csegclass, and
        2. all cseg similarity in previous list.

        Accepts built classes with one cardinality
        """

        csegclasses = []
        similarity = []

        for (a, b, csegclass, d) in built_classes:
            csegclass = contour.Contour(csegclass)
            csim = cseg_similarity(cseg, csegclass)
            csegclasses.append([csim, csegclass])
            similarity.append(csim)

        return csegclasses, sorted(list(set(similarity)))

    def grouped_cseg_similarity_lists((csegclasses, similarity)):
        """Returns csegclasses grouped by cseg similarity. Accepts
        lists provided by cseg_similarity_lists function.
        """

        result = []

        for similarity_index in similarity:
            simil_index = []
            for csegclass in sorted(csegclasses):
                if csegclass[0] == similarity_index:
                    simil_index.append(csegclass[1])
            result.append([similarity_index, simil_index])

        return result

    return grouped_cseg_similarity_lists(cseg_similarity_lists(built_classes))


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
        prime = contour.Contour(subset)
        acmemb = all_contour_mutually_embed(cseg, prime)
        result.append([prime, acmemb])

    return sorted(result, key=lambda x: x[1])
