# -*- coding: utf-8 -*-

import unittest
import contour.matrix as matrix
from contour.matrix import ComparisonMatrix
from contour.matrix import FuzzyMatrix
from contour.matrix import InternalDiagonal
from contour.contour import Contour
from contour import _utils


class TestUtils(unittest.TestCase):
    # diagonal
    def test_csegs(self):
        i1 = InternalDiagonal([-1, 1])
        i2 = InternalDiagonal([-1, 1, 1])
        self.assertEqual(i1.csegs(), [Contour([1, 0, 2]), Contour([2, 0, 1])])
        self.assertEqual(i2.csegs(), [Contour([1, 0, 2, 3]), Contour([2, 0, 1, 3]),
                                      Contour([3, 0, 1, 2])])

    def test_inversion_Int(self):
        i1 = InternalDiagonal([-1, 1])
        i2 = InternalDiagonal([-1, 1, 1])
        self.assertEqual(i1.inversion(), InternalDiagonal([1, -1]))
        self.assertEqual(i2.inversion(), InternalDiagonal([1, -1, -1]))

    def test_rotation_Int(self):
        i1 = InternalDiagonal([1, 1, 0, -1, -1, 1])
        i2 = InternalDiagonal([1, 1, 0, -1, -1, 1])
        i3 = InternalDiagonal([1, 1, 0, -1, -1, 1])
        i4 = InternalDiagonal([1, 1, 0, -1, -1, 1])
        self.assertEqual(i1.rotation(), InternalDiagonal([1, 0, -1, -1, 1, 1]))
        self.assertEqual(i2.rotation(1), InternalDiagonal([1, 0, -1, -1, 1, 1]))
        self.assertEqual(i3.rotation(2), InternalDiagonal([0, -1, -1, 1, 1, 1]))
        self.assertEqual(i4.rotation(20), InternalDiagonal([0, -1, -1, 1, 1, 1]))

    def test_Int_subsets(self):
        i = InternalDiagonal([1, 1, 0, -1, -1, 1])
        result1 = [[-1, -1], [-1, 1], [-1, 1], [0, -1], [0, -1],
                   [0, 1], [1, -1], [1, -1], [1, -1], [1, -1],
                   [1, 0], [1, 0], [1, 1], [1, 1], [1, 1]]
        result2 = [[-1, -1, 1], [0, -1, -1], [0, -1, 1], [0, -1, 1],
                   [1, -1, -1], [1, -1, -1], [1, -1, 1], [1, -1, 1],
                   [1, -1, 1], [1, -1, 1], [1, 0, -1], [1, 0, -1],
                   [1, 0, -1], [1, 0, -1], [1, 0, 1], [1, 0, 1],
                   [1, 1, -1], [1, 1, -1], [1, 1, 0], [1, 1, 1]]
        self.assertEqual(i.subsets(2), result1)
        self.assertEqual(i.subsets(3), result2)

    def test_Int_all_subsets(self):
        i = InternalDiagonal([1, 1, 0, -1, -1, 1])
        result = [[-1, -1], [-1, 1], [-1, 1], [0, -1], [0, -1],
                  [0, 1], [1, -1], [1, -1], [1, -1], [1, -1],
                  [1, 0], [1, 0], [1, 1], [1, 1], [1, 1],
                  [-1, -1, 1], [0, -1, -1], [0, -1, 1],
                  [0, -1, 1], [1, -1, -1], [1, -1, -1],
                  [1, -1, 1], [1, -1, 1], [1, -1, 1], [1, -1, 1],
                  [1, 0, -1], [1, 0, -1], [1, 0, -1], [1, 0, -1],
                  [1, 0, 1], [1, 0, 1], [1, 1, -1], [1, 1, -1],
                  [1, 1, 0], [1, 1, 1], [0, -1, -1, 1],
                  [1, -1, -1, 1], [1, -1, -1, 1], [1, 0, -1, -1],
                  [1, 0, -1, -1], [1, 0, -1, 1], [1, 0, -1, 1],
                  [1, 0, -1, 1], [1, 0, -1, 1], [1, 1, -1, -1],
                  [1, 1, -1, 1], [1, 1, -1, 1], [1, 1, 0, -1],
                  [1, 1, 0, -1], [1, 1, 0, 1], [1, 0, -1, -1, 1],
                  [1, 0, -1, -1, 1], [1, 1, -1, -1, 1],
                  [1, 1, 0, -1, -1], [1, 1, 0, -1, 1],
                  [1, 1, 0, -1, 1], [1, 1, 0, -1, -1, 1]]
        self.assertEqual(i.all_subsets(), result)

    def test_Int_subsets_adj_1(self):
        i = InternalDiagonal([1, 1, 0, -1, -1, 1])
        result1 = [[1, 1], [1, 0], [0, -1], [-1, -1], [-1, 1]]
        result2 = [[1, 1, 0], [1, 0, -1], [0, -1, -1], [-1, -1, 1]]
        self.assertEqual(i.subsets_adj(2), result1)
        self.assertEqual(i.subsets_adj(3), result2)

    def test_csegs_from_diagonals(self):
        d = [InternalDiagonal([1, -1, 1, -1]), InternalDiagonal([1, 1, 1]),
             InternalDiagonal([1, 1]), InternalDiagonal([1])]
        self.assertEqual(matrix.csegs_from_diagonals(d), Contour([0, 2, 1, 4, 3]))

    # crisp
    def test_Com_matrix_cseg(self):
        cm = ComparisonMatrix([[0, 1, 1, 1], [-1, 0, -1, 1], [-1, 1, 0, 1], [-1, -1, -1, 0]])
        self.assertEqual(cm.cseg(), Contour([0, 2, 1, 3]))

    def test_Com_matrix_diagonal(self):
        cm = ComparisonMatrix([[0, 1, 1, 1], [-1, 0, -1, 1], [-1, 1, 0, 1], [-1, -1, -1, 0]])
        self.assertEqual(cm.diagonal(), InternalDiagonal([1, -1, 1]))

    def test_Com_matrix_superior_triangle(self):
        cm = ComparisonMatrix([[0, 1, 1, 1], [-1, 0, -1, 1], [-1, 1, 0, 1], [-1, -1, -1, 0]])
        self.assertEqual(cm.superior_triangle(), ComparisonMatrix([[1, 1, 1], [-1, 1], [1]]))
        self.assertEqual(cm.superior_triangle(2), ComparisonMatrix([[1, 1], [1]]))

    def test_Com_matrix_fuzzy_matrix(self):
        cm = ComparisonMatrix([[0, 1, 1, 1], [-1, 0, -1, 1], [-1, 1, 0, 1], [-1, -1, -1, 0]])
        fz = FuzzyMatrix([[0, 1, 1, 1], [0, 0, 0, 1], [0, 1, 0, 1], [0, 0, 0, 0]])
        self.assertEqual(cm.fuzzy_matrix(), fz)

    def test_matrix_from_triangle(self):
        tri = [[1, 1, 1, 1], [1, 1, 1], [-1, -1], [1]]
        result = ComparisonMatrix([[0, 1, 1, 1, 1],
                                   [-1, 0, 1, 1, 1],
                                   [-1, -1, 0, -1, -1],
                                   [-1, -1, 1, 0, 1],
                                   [-1, -1, 1, -1, 0]])
        self.assertEqual(matrix._matrix_from_triangle(tri), result)

    def test_triangle_zero_replace(self):
        triangle = [[1, 0, 1, 1], [1, 0, 1], [1, 0], [1]]
        result = ComparisonMatrix([[1, -1, 1, 1], [1, -1, 1], [1, -1], [1]])
        self.assertEqual(matrix._triangle_zero_replace(triangle, -1), result)

    def test_triangle_zero_replace_to_cseg(self):
        triangle = [[1, 1, 1, 1], [1, 0, 1], [-1, 0], [1]]
        cseg1, cseg2 = Contour([0, 1, 3, 2, 4]), Contour([0, 2, 4, 1, 3])
        self.assertEqual(matrix._triangle_zero_replace_to_cseg(triangle), [cseg1, cseg2])

    # fuzzy
    def test__FuzzyMatrix_except_zero_diagonal(self):
        f = [[0, 1, 1, 1], [0, 0, 1, 1], [0, 0, 0, 0], [0, 0, 1, 0]]
        self.assertEqual(FuzzyMatrix(f).except_zero_diagonal(), [[1, 1, 1], [0, 1, 1],
                                                                       [0, 0, 0], [0, 0, 1]])

    def test__comparison(self):
        f1 = [[0, 1, 1], [0, 0, 0], [0, 1, 0]]
        f2 = [[0.0, 0.0, 0.0, 0.0, 0.0],
             [1.0, 0.0, 1.0, 1.0, 0.66666666666666663],
             [1.0, 0.0, 0.0, 1.0, 0.33333333333333331],
             [1.0, 0.0, 0.0, 0.0, 0.0],
             [1.0, 0.33333333333333331, 0.33333333333333331, 1.0, 0.0]]
        result1 = [[0, 1, 1], [-1, 0, -1], [-1, 1, 0]]
        result2 = [[0.0, -1.0, -1.0, -1.0, -1.0],
                  [1.0, 0.0, 1.0, 1.0, 0.3333333333333333],
                  [1.0, -1.0, 0.0, 1.0, 0.0],
                  [1.0, -1.0, -1.0, 0.0, -1.0],
                  [1.0, -0.3333333333333333, 0.0, 1.0, 0.0]]
        self.assertEqual(FuzzyMatrix(f1).comparison(), result1)
        self.assertEqual(FuzzyMatrix(f2).comparison(), result2)

    def test__average_matrix(self):
        cseg1 = Contour([3, 0, 1, 2, 1])
        cseg2 = Contour([4, 0, 1, 3, 2])
        cseg3 = Contour([4, 1, 2, 3, 0])
        result = [[0.0, 0.0, 0.0, 0.0, 0.0],
                  [1.0, 0.0, 1.0, 1.0, 0.66666666666666663],
                  [1.0, 0.0, 0.0, 1.0, 0.33333333333333331],
                  [1.0, 0.0, 0.0, 0.0, 0.0],
                  [1.0, 0.33333333333333331, 0.33333333333333331, 1.0, 0.0]]
        self.assertEqual(matrix.average_matrix(cseg1, cseg2, cseg3), result)

    def test__average_matrix_desert_music(self):
        # Quinn 1997, table 4, second matrix
        m1 = Contour([5, 4, 3, 6, 1, 2, 3, 2, 4, 3, 0])
        m2a = Contour([6, 7, 4, 3, 0, 2, 1, 0, 3, 4, 5])
        m2b = Contour([5, 7, 4, 3, 0, 2, 1, 0, 3, 4, 6])
        m3a = Contour([7, 6, 4, 1, 5, 3, 0, 2, 4, 5, 3])
        m3b = Contour([4, 6, 5, 3, 2, 6, 5, 1, 0, 6, 5])
        m4a = Contour([8, 7, 5, 6, 3, 5, 4, 0, 2, 5, 1])
        m4b = Contour([7, 6, 4, 5, 4, 3, 1, 0, 3, 5, 2])
        m5 = Contour([7, 3, 6, 5, 4, 1, 0, 2, 4, 2, 4])
        m6a = Contour([7, 5, 2, 0, 1, 3, 6, 5, 4, 3, 1])
        m6b = Contour([8, 6, 3, 0, 1, 5, 7, 6, 5, 4, 2])
        m6c = Contour([8, 6, 3, 2, 4, 6, 7, 5, 2, 0, 1])
        m7a = Contour([8, 6, 4, 2, 7, 4, 1, 3, 0, 2, 5])
        m7b = Contour([6, 5, 3, 1, 4, 2, 0, 1, 3, 4, 2])
        m8a = Contour([7, 5, 2, 7, 6, 4, 1, 0, 2, 5, 3])
        m8b = Contour([7, 5, 3, 7, 6, 2, 1, 0, 3, 5, 4])
        m8c = Contour([6, 4, 2, 6, 5, 3, 1, 0, 2, 4, 3])
        csegs = [m1, m2a, m2b, m3a, m3b, m4a, m4b, m5, m6a, m6b, m6c, m7a, m7b, m8a, m8b, m8c]
        ocurrences = [14, 9, 3, 10, 3, 10, 3, 14, 8, 2, 2, 9, 4, 9, 2, 2]
        # weight csegs by ocurrences number
        weight_csegs = _utils.flatten([[cseg for i in range(o)] for cseg, o in zip(csegs, ocurrences)])
        weight_average = matrix.average_matrix(*weight_csegs)
        # round numbers like table 4
        rounded = [[round(x, 2) for x in row] for row in weight_average]
        result = [[0.0, 0.14, 0.03, 0.13, 0.0, 0.03, 0.03, 0.0, 0.0, 0.03, 0.06],
                  [0.86, 0.0, 0.13, 0.39, 0.35, 0.0, 0.12, 0.0, 0.13, 0.0, 0.13],
                  [0.97, 0.87, 0.0, 0.38, 0.37, 0.25, 0.12, 0.12, 0.23, 0.41, 0.33],
                  [0.74, 0.61, 0.62, 0.0, 0.34, 0.37, 0.14, 0.3, 0.23, 0.38, 0.46],
                  [1.0, 0.65, 0.61, 0.66, 0.0, 0.49, 0.49, 0.25, 0.35, 0.5, 0.16],
                  [0.97, 0.95, 0.57, 0.63, 0.51, 0.0, 0.25, 0.23, 0.62, 0.67, 0.36],
                  [0.97, 0.88, 0.72, 0.86, 0.51, 0.75, 0.0, 0.36, 0.67, 0.75, 0.63],
                  [1.0, 0.9, 0.88, 0.66, 0.63, 0.63, 0.64, 0.0, 0.77, 0.66, 0.75],
                  [1.0, 0.73, 0.51, 0.63, 0.52, 0.34, 0.33, 0.23, 0.0, 0.62, 0.36],
                  [0.97, 0.85, 0.24, 0.51, 0.37, 0.13, 0.12, 0.2, 0.38, 0.0, 0.36],
                  [0.94, 0.87, 0.64, 0.54, 0.63, 0.49, 0.35, 0.25, 0.51, 0.64, 0.0]]
        self.assertEqual(rounded, result)

if __name__ == '__main__':
    unittest.main()
