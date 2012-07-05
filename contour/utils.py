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


def percent(seq):
    """Outputs percentuals from a sequence.

    >>> percent()[[(1, 0), 10], [(0, 1), 11]]
    [[(1, 0), '47.62'], [(0, 1), '52.38']]
    """

    sigma = sum(x[1] for x in seq)
    return [[n[0], "%.2f" % (float(n[1]) * 100 / sigma)] for n in seq]


def lists_printing(seq):
    """Prints a sequence of two items sequences.

    >>> lists_printing([[0, 1], [2, 3], [4, 5]])
    0 - 1 %
    2 - 3 %
    4 - 5 %
    """

    for n in seq:
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


def replace_list_to_plus_minus(seq):
    """Convert a sequence in a string and replace -1 by -, and 1 by +

    >>> replace_list_to_plus_minus([1, 1, -1, -1])
    '+ + - -'
    """

    return " ".join([double_replace(str(x)) for x in seq])


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


def list_to_string(seq):
    """Convert a sequence in a string.

    >>> list_to_string([1, 2, 3])
    '1 2 3'
    """

    return " ".join([str(x) for x in seq])


def remove_adjacent(seq):
    """Removes duplicate adjacent elements from a sequence.

    >>> remove_adjacent([0, 1, 1, 2, 3, 1, 4, 2, 2, 5])
    [0, 1, 2, 3, 1, 4, 2, 5]
    """

    groups = itertools.izip(seq, seq[1:])
    return [a for a, b in groups if a != b] + [seq[-1]]


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


def pretty_as_cseg(seq):
    """Prints like cseg, used in Contour theories.

    >>> pretty_as_cseg([1, 3, 5, 4])
    < 1 3 5 4 >
    """

    return "< " + list_to_string(seq) + " >"


def greatest_first(seq1, seq2):
    """Returns greatest sequence first.

    >>> greatest_first([0, 1], [3, 2, 1])
    [[3, 2, 1], [0, 1]]
    """

    if len(seq1) > len(seq2):
        return [seq1, seq2]
    else:
        return [seq2, seq1]


def permut_list(numbers_list):
    """Returns a sorted list of all permutations of a list.

    >>> permut_list([1, 2, 3])
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """

    permutted = sorted(itertools.permutations(numbers_list, len(numbers_list)))
    return [list(x) for x in permutted]


def with_index(seq):
    """Returns a generator from a sequence."""

    for i in xrange(len(seq)):
        yield i, seq[i]


def replace_all(seq, replacement):
    """Replace all zeros in a sequence by a given replacement element.

    >>> replace_all([0, 3, 2, 0], -1)
    [-1, 3, 2, -1]
    """

    new_seq = seq[:]

    for i, elem in with_index(new_seq):
        if elem == 0:
            new_seq[i] = replacement
    return new_seq


def negative(num):
    return num * -1

def addition(a, b):
    return a + b

def difference(a, b):
    return b - a

def multiplication(a, b):
    return a * b

def quotient(a, b):
    try:
        return b / float(a)
    except:
        print "Number error"

def seq_operation(fn, seq):
    return [fn(a, b) for a, b in zip(seq, seq[1:])]


def rotation(obj, factor):
    n = factor % obj.size()
    return obj[n:] + obj[:n]
