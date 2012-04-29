# -*- coding: utf-8 -*-

import unittest
import contour.utils as utils


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

if __name__ == '__main__':
    unittest.main()
