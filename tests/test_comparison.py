# -*- coding: utf-8 -*-

import unittest
import contour.comparison as comparison
from contour.contour import Contour
from contour.matrix import InternalDiagonal


class TestUtils(unittest.TestCase):
    def test_cseg_similarity(self):
        cseg1 = Contour([0, 2, 3, 1])
        cseg2 = Contour([3, 1, 0, 2])
        cseg3 = Contour([1, 0, 4, 3, 2])
        cseg4 = Contour([3, 0, 4, 2, 1])
        cseg5 = Contour([0, 1, 2, 3, 4, 5, 6])
        cseg6 = Contour([2, 6, 5, 4, 1, 0, 3])
        self.assertEqual(comparison.cseg_similarity(cseg1, cseg2), 0)
        self.assertEqual(comparison.cseg_similarity(cseg3, cseg4), 0.8)
        self.assertEqual(comparison.cseg_similarity(cseg5, cseg6), 0.2857142857142857)

    def test_csegclass_similarity(self):
        cseg1 = Contour([0, 2, 3, 1])
        cseg2 = Contour([3, 1, 0, 2])
        self.assertEqual(comparison.csegclass_similarity(cseg1, cseg2), 1)

    def test_cseg_similarity_matrix(self):
        cseg1 = Contour([1, 0, 4, 3, 2])
        cseg2 = Contour([3, 0, 4, 2, 1])
        result = [[Contour([1, 0, 4, 3, 2]), Contour([3, 0, 4, 2, 1])],
                  [1.0, 0.8], [0.8, 1.0]]
        self.assertEqual(comparison.cseg_similarity_matrix([cseg1, cseg2]), result)

    def test_cseg_similarity_matrix_classes(self):
        result = [[Contour([0, 1, 2]), Contour([0, 2, 1])], [1.0, 0.66666666666666663],
                  [0.66666666666666663, 1.0]]
        self.assertEqual(comparison.cseg_similarity_matrix_classes(3), result)

    def test_csubseg_mutually_embedded(self):
        cseg1 = Contour([1, 0, 4, 3, 2])
        cseg2 = Contour([2, 0, 1, 4, 3])
        self.assertEqual(comparison.cseg_mutually_embedded(3, cseg1, cseg2), 16)
        self.assertEqual(comparison.cseg_mutually_embedded(4, cseg1, cseg2), 5)

    def test_all_cseg_mutually_embedded(self):
        cseg1 = Contour([0, 1, 2, 3])
        cseg2 = Contour([0, 2, 1, 3])
        cseg3 = Contour([0, 2, 1, 3, 4])
        cseg4 = Contour([0, 1, 0])
        cseg5 = Contour([0, 1, 2, 0])
        self.assertEqual(comparison.all_cseg_mutually_embedded(cseg1, cseg2), 17.0 / 22)
        self.assertEqual(comparison.all_cseg_mutually_embedded(cseg1, cseg3), 29.0 / 37)
        self.assertEqual(comparison.all_cseg_mutually_embedded(cseg2, cseg3), 33.0 / 37)
        self.assertEqual(comparison.all_cseg_mutually_embedded(cseg4, cseg5), 0.8)

    def test_cseg_similarity_continuum(self):
        result = [[0.0, [Contour([2, 3, 0, 1])]],
                  [0.16666666666666666, [Contour([1, 3, 0, 2]),
                                         Contour([2, 3, 1, 0]),
                                         Contour([3, 2, 0, 1])]],
                  [0.3333333333333333, [Contour([0, 3, 1, 2]),
                                        Contour([1, 2, 0, 3]),
                                        Contour([1, 3, 2, 0]),
                                        Contour([3, 1, 0, 2]),
                                        Contour([3, 2, 1, 0])]],
                  [0.5, [Contour([0, 2, 1, 3]),
                         Contour([0, 3, 2, 1]),
                         Contour([1, 2, 3, 0]),
                         Contour([2, 1, 0, 3]),
                         Contour([3, 0, 1, 2]),
                         Contour([3, 1, 2, 0])]],
                  [0.6666666666666666, [Contour([0, 1, 2, 3]),
                                        Contour([0, 2, 3, 1]),
                                        Contour([2, 0, 1, 3]),
                                        Contour([2, 1, 3, 0]),
                                        Contour([3, 0, 2, 1])]],
                  [0.8333333333333334, [Contour([0, 1, 3, 2]),
                                        Contour([1, 0, 2, 3]),
                                        Contour([2, 0, 3, 1])]],
                  [1.0, [Contour([1, 0, 3, 2])]]]
        self.assertEqual(comparison.cseg_similarity_continuum(Contour([1, 0, 3, 2])), result)

    def test_cseg_similarity_subsets_continuum(self):
        result = [[Contour([0, 1]), 0.5833333333333334],
                  [Contour([0, 1, 2]), 0.9333333333333333],
                  [Contour([0, 1, 2, 3]), 1.0]]
        self.assertEqual(comparison.cseg_similarity_subsets_continuum(Contour([0, 1, 2, 3])), result)

    def test_entry_numbers(self):
        self.assertEqual(comparison.entry_numbers(5), 20)

    def test_entry_numbers_cseg(self):
        self.assertEqual(comparison.entry_numbers_cseg(Contour([2, 0, 3, 1, 4])), 20)

    def test_similarity_increment(self):
        self.assertEqual(comparison.similarity_increment(0.8, 0.9, 2), 0.45)

    def test_fuzzy_similarity_matrix(self):
        self.assertEqual(comparison.fuzzy_similarity_matrix([[0, 0.8], [0, 0]], [[0, 0.9], [0, 0]]), 0.95)

    def test_fuzzy_similarity(self):
        cseg1 = Contour([4, 1, 2, 3, 0])
        cseg2 = Contour([4, 0, 1, 3, 2])
        self.assertEqual(comparison.fuzzy_similarity(cseg1, cseg2), 0.8000000000000002)

if __name__ == '__main__':
    unittest.main()
