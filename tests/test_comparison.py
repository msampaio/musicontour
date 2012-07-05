# -*- coding: utf-8 -*-

import unittest
import contour.comparison as comparison
from contour.contour import Contour
from contour.diagonal import InternalDiagonal


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

    def test_subsets_embedded_total_number(self):
        cseg1 = Contour([0, 1, 2, 3])
        cseg2 = Contour([1, 0, 2])
        cseg3 = Contour([0, 1, 3, 2])
        cseg4 = Contour([1, 0, 2])
        self.assertEqual(comparison.subsets_embedded_total_number(cseg1, cseg2), 4)
        self.assertEqual(comparison.subsets_embedded_total_number(cseg3, cseg4), 4)

    # def test_subsets_embedded_number(self):
    #     cseg1 = Contour([0, 2, 1, 3])
    #     cseg2 = Contour([0, 1, 2])
    #     self.assertEqual(comparison.subsets_embedded_number(cseg1, cseg2), 2)

    # def test_contour_embedded(self):
    #     cseg1 = Contour([0, 2, 1, 3])
    #     cseg2 = Contour([0, 1, 2])
    #     cseg3 = Contour([0, 2, 1, 3, 4])
    #     cseg4 = Contour([0, 1, 2])
    #     self.assertEqual(comparison.contour_embedded(cseg1, cseg2), 0.5)
    #     self.assertEqual(comparison.contour_embedded(cseg3, cseg4), 0.7)

    # def test_contour_similarity_compare(self):
    #     cseg1 = Contour([0, 2, 1, 3])
    #     cseg2 = Contour([0, 1, 2])
    #     cseg3 = Contour([0, 1, 2, 4])
    #     self.assertEqual(comparison.cseg_similarity_compare(cseg1, cseg2), ["Cseg embedded", 0.5])
    #     self.assertEqual(comparison.cseg_similarity_compare(cseg1, cseg3), ["Cseg similarity", 5 / 6.0])

    def test_csubseg_mutually_embedded(self):
        cseg1 = Contour([1, 0, 4, 3, 2])
        cseg2 = Contour([2, 0, 1, 4, 3])
        self.assertEqual(comparison.csubseg_mutually_embedded(3, cseg1, cseg2), 0.8)
        self.assertEqual(comparison.csubseg_mutually_embedded(4, cseg1, cseg2), 0.5)

    def test_all_contour_mutually_embedded(self):
        cseg1 = Contour([0, 1, 2, 3])
        cseg2 = Contour([0, 2, 1, 3])
        cseg3 = Contour([0, 2, 1, 3, 4])
        cseg4 = Contour([0, 1, 0])
        cseg5 = Contour([0, 1, 2, 0])
        self.assertEqual(comparison.all_contour_mutually_embedded(cseg1, cseg2), 17.0 / 22)
        self.assertEqual(comparison.all_contour_mutually_embedded(cseg1, cseg3), 29.0 / 37)
        self.assertEqual(comparison.all_contour_mutually_embedded(cseg2, cseg3), 33.0 / 37)
        self.assertEqual(comparison.all_contour_mutually_embedded(cseg4, cseg5), 0.8)

    # def test_operations_comparison(self):
    #     cseg1, cseg2 = Contour([0, 1, 2, 3]), Contour([3, 1, 2, 0])
    #     result = [[(Contour([0, 1, 2, 3]), 2, 'internal_diagonals', InternalDiagonal([1, -1, 1])),
    #                (Contour([3, 1, 2, 0]), 1, 'internal_diagonals', InternalDiagonal([1, -1, 1]))]]
    #     self.assertEqual(comparison.operations_comparison(cseg1, cseg2), result)

    # def test_pretty_operations_comparison(self):
    #     cseg1 = Contour([0, 1, 2, 3])
    #     cseg2 = Contour([3, 1, 2, 0])
    #     result = '< 0 1 2 3 > [rot1] (internal_diagonals): < + - + >\n' + \
    #                  '< 3 1 2 0 > [rot1] (internal_diagonals)\n'
    #     self.assertEqual(comparison.pretty_operations_comparison(cseg1, cseg2), result)

    # def test_cseg_similarity_continuum(self):
    #     result = [[0.5, [Contour([0, 2, 1, 3]), Contour([0, 3, 2, 1])]],
    #               [0.66666666666666663, [Contour([0, 1, 2, 3]), Contour([0, 2, 3, 1]),
    #                                      Contour([0, 3, 1, 2])]],
    #               [0.83333333333333337, [Contour([0, 1, 3, 2]), Contour([1, 3, 0, 2])]],
    #               [1.0, [Contour([1, 0, 3, 2])]]]
    #     self.assertEqual(comparison.cseg_similarity_continuum(Contour([1, 0, 3, 2])), result)

    # def test_cseg_similarity_subsets_continuum(self):
    #     result = [[Contour([0, 1]), 0.58333333333333337],
    #               [Contour([0, 1, 2]), 0.93333333333333335],
    #               [Contour([0, 1, 2, 3]), 1.0]]
    #     self.assertEqual(comparison.cseg_similarity_subsets_continuum(Contour([0, 1, 2, 3])), result)

if __name__ == '__main__':
    unittest.main()
