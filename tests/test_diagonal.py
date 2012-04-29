# -*- coding: utf-8 -*-

import unittest
from contour.diagonal import InternalDiagonal
import contour.diagonal as diagonal
from contour.contour import Contour

class TestUtils(unittest.TestCase):
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
        self.assertEqual(diagonal.csegs_from_diagonals(d), [0, 2, 1, 4, 3])

if __name__ == '__main__':
    unittest.main()
