#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import contour


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
    return num * - 1

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


def make_matrix(fn, obj):
    return [[fn([a.value, b.value]) for b in obj] for a in obj]


notes = "c c# d d# e f f# g g# a a# b".split()


def permut_csegs(cardinality):
    """Returns a list of possible normalized csegs of a given
    cardinality. Cseg are output as lists.

    >>> permut_csegs(3)
    [[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]
    """

    base = range(cardinality)
    return permut_list(base)


def apply_fn(obj, fn):
    """Apply a method to a contour object.

    >>> apply_fn(Contour([0, 1, 2]), 'retrogression')
    < 2 1 0 >
    """

    return apply(getattr(contour.Contour(obj.cseg), fn))


def absolute_pitches(cseg, pitch_set):
    """Returns absolute pitches for given cseg and pitch set with the
    same cardinality.

    >>> absolute_pitches(Contour([1, 4, 2, 3, 0]), [0, 7, 6, 9, 4])
    [12, 31, 18, 21, 4]
    """

    # lists stores [position, cpitch, pitch] for each pitch
    lists = [[pos, cseg[pos], value] for (pos, value) in enumerate(pitch_set)]
    lists = sorted(lists, key=lambda x: x[1])

    for el in range(1, len(lists)):
        interval = lists[el][2] - lists[el - 1][2]
        # increases octaves if interval between a pitch and previous
        # is negative
        if interval < 0:
            octave = abs(interval / 12) * 12
            lists[el] = [lists[el][0], lists[el][1], (lists[el][2] + octave)]
    return [x[2] for x in sorted(lists, key=lambda x: x[0])]


def absolute_pitches_permutation(cseg, psets_list):
    """Returns lists of absolute pitches permutations of a given cseg
    and a list of pitch sets permutations.

    >>> absolute_pitches_permutation(Contour([0, 1, 2]), [3, 4, 5])
    [[3, 4, 5], [3, 5, 16], [4, 15, 17], [4, 5, 15], [5, 15, 16], [5, 16, 27]]
    """

    permutted = permut_list(psets_list)
    return [absolute_pitches(cseg, pset) for pset in permutted]


def octave_calculator(pitch):
    """Returns pitch class and octave for a given absolute pitch.

    >>> octave_calculator(50)
    (2, 4)
    """

    p_class = pitch % 12
    octave = pitch / 12
    return (p_class, octave)


def simple_contour(*args):
    """Returns a Contour object from given args.

    >>> simple_contour(0, 1, 2)
    < 0 1 2 >
    """

    return contour.Contour(list(args))


def cseg_string_to_Contour(cseg_string):
    """Returns a Contour object from a cseg string:

    >>> cseg_string_to_Contour('< 0 1 2 >')
    Contour([0, 1, 2])
    """

    splitted = cseg_string.strip("<").strip(">").split()

    return contour.Contour([int(x) for x in splitted])


def absolute_pitch_from_note_octave(note, octave):
    """Returns an absolute pitch from a given note and octave

    >>> note_to_absolute_pitch(1, 4)
    49
    """

    try:
        return note + (octave * 12)
    except:
        pass


def absolute_pitch_from_str(note_string, notes=notes):
    """Returns an absolute pitch from a given string with a note.

    >>> absolute_pitch('d#4')
    51
    """

    note = notes.index(note_string[:-1])
    octave = int(note_string[-1])

    return absolute_pitch_from_note_octave(note, octave)


def notes_to_Contour(notes_string):
    """Returns Contour object from a given string with notes.

    >>> notes_to_Contour('c4 d3 e5')
    < 1 0 2 >
    """

    splt = notes_string.split()
    cseg = contour.Contour([absolute_pitch_from_str(note) for note in splt])
    return cseg.translation()


def cseg_from_class_number(card, class_number, prime_algorithm="prime_form_sampaio"):
    """Returns a cseg from a given cardinality and class
    number. Sampaio Prime algorithm is default.

    >>> cseg_from_class_number(4, 7)
    < 1 0 3 2 >
    """

    card_classes = contour.build_classes_card(card, prime_algorithm)
    for classes in card_classes:
        cc, cn, cs, ri = classes
        if card == cc and class_number == cn:
            return contour.Contour(cs)


def position_comparison(list_1, list_2):
    """Returns a similarity index based on the number of equal
    elements in same positions in two lists.

    >>> position_comparison([0, 1, 2, 3], [0, 1, 3, 2])
    0.5
    """

    value = 0
    size = len(list_1)
    for pos in range(size):
        if list_1[pos] == list_2[pos]:
            value += 1
    return value / float(size)


def base_3_comparison(a, b):
    """Returns comparison in base three (0, 1, 2).

    >>> base_3_comparison(4, 5)
    2
    """

    return cmp(b, a) + 1


def ascent_membership(el):
    """Returns fuzzy ascent membership from a crisp relation.

    >>> ascent_membership(-1)
    0
    """

    if el in (-1, 0):
        return 0
    elif el == 1:
        return 1
    else:
        print el, "is not a crisp relation."


def count_sets(seq1, seq2):
    """Return the number of times ordered seq1 is in ordered seq2.

    >>> count_sets([1, 2], [1, 2, 3, 4, 1, 5, 2])
    3
    """
    if seq1 == []:
        return 1
    elif seq2 == []:
        return 0
    elif seq1[0] == seq2[0]:
        return count_sets(seq1[1:], seq2[1:]) + count_sets(seq1, seq2[1:])
    else:
        return count_sets(seq1, seq2[1:])
