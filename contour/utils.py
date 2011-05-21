#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import itertools


def flatten(seq):
    """Flatten Sequences.

    >>> flatten([[0, 1], [2, 3]])
    [0, 1, 2, 3]
    """

    return [item for sublist in seq for item in sublist]


def filter_int(item):
    """Tests and outputs int.

    >>> filter_int(3):
    3
    """

    if isinstance(item, int):
        return item
    else:
        return ''


def percent(list):
    """Outputs percentuals from a list.

    >>> percent()[[(1, 0), 10], [(0, 1), 11]]
    [[(1, 0), '47.62'], [(0, 1), '52.38']]
    """

    sigma = sum(x[1] for x in list)
    return [[n[0], "%.2f" % (float(n[1]) * 100 / sigma)] for n in list]


def lists_printing(list):
    """Prints a list of two items lists.

    >>> lists_printing([[0, 1], [2, 3], [4, 5]])
    0 - 1 %
    2 - 3 %
    4 - 5 %
    """

    for n in list:
        print("{0} - {1} %".format(n[0], n[1]))


def item_count(data):
    """Counts items in a list of lists.

    >>> item_count([[0, 1], [2, 3], [4, 5]])
    [[(0, 1), 1], [(4, 5), 1], [(2, 3), 1]]
    """

    sorted_subsets = sorted(data)
    tuples = [tuple(x) for x in sorted_subsets]
    contour_type = list(set(tuples))
    counted_contours = [[x, tuples.count(x)] for x in contour_type]
    return sorted(counted_contours, key=lambda x: x[1], reverse=True)


# FIXME: Remove function?
def abcm2ps(path, abc_filename):
    filename = abc_filename.split(".abc")[0]
    abc_file = path + "/" + abc_filename
    ps_file = path + "/" + filename + ".ps"
    subprocess.call('abcm2ps -O {0} {1}'.format(ps_file, abc_file), shell=True)


def double_replace(string):
    """Replaces -1 by -, and 1 by +. Accepts string as input.

    >>> double_replace('-1 1 -1 1')
    '- + - +'
    """

    return string.replace("-1", "-").replace("1", "+")


def replace_list_to_plus_minus(list):
    """Convert a list in a string and replace -1 by -, and 1 by +

    >>> replace_list_to_plus_minus([1, 1, -1, -1])
    '+ + - -'
    """

    return " ".join([double_replace(str(x)) for x in list])


def replace_plus_minus_to_list(string):
    """Convert a string with - and + to a list with -1, and 1.

    >>> replace_plus_minus_to_list(\"- + -\")
    [-1, 1, -1]]
    >>> replace_plus_minus_to_list(\"-1 1 - + -\")
    [-1, 1, -1, 1, -1]]
    """

    partial1 = string.replace('-1', '-').replace('1', '+')
    partial2 = partial1.replace('-', '-1').replace('+', '1')
    return [int(x) for x in partial2.split(" ") if x]


def list_to_string(list):
    """Convert a list in a string.

    >>> list_to_string([1, 2, 3])
    '1 2 3'
    """

    return " ".join([str(x) for x in list])


def remove_adjacent(list):
    """Removes duplicate adjacent elements from a list.

    >>> remove_adjacent([0, 1, 1, 2, 3, 1, 4, 2, 2, 5])
    [0, 1, 2, 3, 1, 4, 2, 5]
    """

    groups = itertools.izip(list, list[1:])
    return [a for a, b in groups if a != b] + [list[-1]]


def remove_duplicate_tuples(list_of_tuples):
    """Removes tuples that the first item is repeated in adjacent
    tuples. The removed tuple is the second.

    >>> remove_duplicate_tuples([(0, 1), (0, 2), (1, 3), (2, 4), (1, 5)])
    [(0, 1), (1, 3), (2, 4), (1, 5)]
    """

    prev = None
    tmp = []
    for a, b in list_of_tuples:
        if a != prev:
            tmp.append((a, b))
            prev = a
    return tmp


def pretty_as_cseg(list):
    """Prints like cseg, used in Contour theories.

    >>> pretty_as_cseg([1, 3, 5, 4])
    < 1 3 5 4 >
    """

    return "< " + list_to_string(list) + " >"


def greatest_first(list1, list2):
    """Returns greatest list first.

    >>> greatest_first([0, 1], [3, 2, 1])
    [[3, 2, 1], [0, 1]]
    """

    if len(list1) > len(list2):
        return [list1, list2]
    else:
        return [list2, list1]


def permut_list(numbers_list):
    """Returns a sorted list of all permutations of a list.

    >>> permut_list([1, 2, 3])
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """

    permutted = sorted(itertools.permutations(numbers_list, len(numbers_list)))
    return [list(x) for x in permutted]


# FIXME: review, test and document these functions
def product_list(vec):
    l = list(itertools.product(*vec))
    return map(lambda x: list(x), l)


def cartesian(a, b):
    ret = []
    for x in a:
        for y in b:
            ret.append(x + y)
    return ret


def generate_plus_minus_1_list(vec):
    if len(vec) == 0:
        return [[]]
    else:
        begin = vec[0:-1]
        last = vec[-1]
        if (last == 0):
            last = [[-1], [1]]
        else:
            last = [[last]]
        return cartesian(generate_plus_minus_1_list(begin), last)


def zero_to_plus_minus(vec):
    result = []
    for subvec in vec:
        result.append(generate_plus_minus_1_list(subvec))
    return product_list(result)
#
