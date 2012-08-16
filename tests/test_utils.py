# -*- coding: utf-8 -*-

import unittest
import contour.__utils as utils


class TestUtils(unittest.TestCase):
    def test_flatten(self):
        result = utils.flatten([[0, 1], [2, 3]])
        self.assertEqual(result, [0, 1, 2, 3])

    def test_filter_int(self):
        self.assertEqual(utils.filter_int(2), 2)
        self.assertEqual(utils.filter_int('a'), '')
        self.assertEqual(utils.filter_int(set()), '')
        self.assertEqual(utils.filter_int({}), '')
        self.assertEqual(utils.filter_int([1, 2]), '')

    def test_percent(self):
        n = [[(1, 0), 10], [(0, 1), 11]]
        self.assertEqual(utils.percent(n), [[(1, 0), '47.62'], [(0, 1), '52.38']])

    def test_item_count(self):
        n = [[0, 1], [2, 3], [4, 5]]
        self.assertEqual(utils.item_count(n), [[(0, 1), 1], [(4, 5), 1], [(2, 3), 1]])

    def test_double_replace(self):
        self.assertEqual(utils.double_replace("0 1 -1 1 0"), "0 + - + 0")

    def test_replace_list_to_plus_minus(self):
        n = [0, 1, 1, -1, -1]
        self.assertEqual(utils.replace_list_to_plus_minus(n), "0 + + - -")

    def test_replace_plus_minus_to_list(self):
        n = "0 + + - -"
        self.assertEqual(utils.replace_plus_minus_to_list(n), [0, 1, 1, -1, -1])

    def test_list_to_string(self):
        self.assertEqual(utils.list_to_string([1, 2, 3]), "1 2 3")

    def test_remove_adjacent(self):
        self.assertEqual(utils.remove_adjacent([1, 4, 9, 9, 2, 1]), [1, 4, 9, 2, 1])
        self.assertEqual(utils.remove_adjacent([0, 1, 1, 2, 3]), [0, 1, 2, 3])
        self.assertEqual(utils.remove_adjacent([1, 4, 9, 9, 2, 4]), [1, 4, 9, 2, 4])

    def test_remove_duplicate_tuples(self):
        n = [(5, 0), (4, 1), (4, 2), (9, 3), (7, 4), (9, 5), (5, 6)]
        result = [(5, 0), (4, 1), (9, 3), (7, 4), (9, 5), (5, 6)]
        self.assertEqual(utils.remove_duplicate_tuples(n), result)

    def test_pretty_as_cseg(self):
        self.assertEqual(utils.pretty_as_cseg([1, 3, 5, 4]), '< 1 3 5 4 >')

    def test_greatest_first(self):
        result = utils.greatest_first([0, 1], [3, 2, 1])
        self.assertEqual(result, [[3, 2, 1], [0, 1]])

    def test_permut_list(self):
        seq = [1, 2, 3]
        result = [seq, [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
        self.assertEqual(utils.permut_list(seq), result)

    def test_replace_all(self):
        list1 = [0, 3, 2, 0]
        self.assertEqual(utils.replace_all(list1, -1), [-1, 3, 2, -1])
        self.assertEqual(utils.replace_all(list1, "a"), ["a", 3, 2, "a"])

    def test_negative(self):
        self.assertEqual(utils.negative(-2), 2)
        self.assertEqual(utils.negative(0), 0)
        self.assertEqual(utils.negative(2), -2)

    def test_addition(self):
        self.assertEqual(utils.addition(-1, 1), 0)
        self.assertEqual(utils.addition(1, 2), 3)

    def test_difference(self):
        self.assertEqual(utils.difference(-1, 1), 2)
        self.assertEqual(utils.difference(1, 1), 0)
        self.assertEqual(utils.difference(1, 3), 2)

    def test_multiplication(self):
        self.assertEqual(utils.multiplication(-2, 3), -6)
        self.assertEqual(utils.multiplication(0, 2), 0)
        self.assertEqual(utils.multiplication(2, 4), 8)

    def test_quotient(self):
        self.assertEqual(utils.quotient(-2, 3), -1.5)
        self.assertEqual(utils.quotient(0, 2), None)
        self.assertEqual(utils.quotient(2, 4), 2)

    def test_seq_operation(self):
        self.assertEqual(utils.seq_operation(utils.addition, [2, 3, 7]), [5, 10])
        self.assertEqual(utils.seq_operation(utils.difference, [2, 3, 7]), [1, 4])
        self.assertEqual(utils.seq_operation(utils.multiplication, [2, 3, 7]), [6, 21])
        self.assertEqual(utils.seq_operation(utils.quotient, [2, 3, 7]), [1.5, 7/float(3)])

    def test_position_comparison(self):
        self.assertEqual(utils.position_comparison([0, 1, 2, 3], [0, 1, 3, 2]), 0.5)

    def test_base_3_comparison(self):
        self.assertEqual(utils.base_3_comparison(1, 0), 0)
        self.assertEqual(utils.base_3_comparison(1, 1), 1)
        self.assertEqual(utils.base_3_comparison(0, 1), 2)

    def test_ascent_membership(self):
        self.assertEqual(utils.ascent_membership(-1), 0)
        self.assertEqual(utils.ascent_membership(0), 0)
        self.assertEqual(utils.ascent_membership(1), 1)

    def test_count_sets(self):
        self.assertEqual(utils.count_sets([], [1, 2]), 1)
        self.assertEqual(utils.count_sets([1], []), 0)
        self.assertEqual(utils.count_sets([1], [2]), 0)
        self.assertEqual(utils.count_sets([1, 2], [1, 2, 3, 1, 4, 2]), 3)

    def test_binomial_coefficient(self):
        self.assertEqual(utils.binomial_coefficient(3, 2), 3)
        self.assertEqual(utils.binomial_coefficient(4, 2), 6)
        self.assertEqual(utils.binomial_coefficient(4, 3), 4)
        self.assertEqual(utils.binomial_coefficient(5, 2), 10)
        self.assertEqual(utils.binomial_coefficient(5, 3), 10)
        self.assertEqual(utils.binomial_coefficient(5, 4), 5)

    def test_number_of_possible_mutually_subsets(self):
        self.assertEqual(utils.number_of_possible_mutually_subsets(2, 2), 2)
        self.assertEqual(utils.number_of_possible_mutually_subsets(3, 2), 5)
        self.assertEqual(utils.number_of_possible_mutually_subsets(3, 3), 8)
        self.assertEqual(utils.number_of_possible_mutually_subsets(4, 3), 15)
        self.assertEqual(utils.number_of_possible_mutually_subsets(4, 4), 22)
        self.assertEqual(utils.number_of_possible_mutually_subsets(5, 4), 37)

if __name__ == '__main__':
    unittest.main()
