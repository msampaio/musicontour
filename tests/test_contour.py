# -*- coding: utf-8 -*-

import unittest
import contour.contour as contour
from contour.contour import ContourPoint as CP
from contour.contour import Contour
from contour.matrix import ComparisonMatrix
from contour.diagonal import InternalDiagonal
from contour.fuzzy import FuzzyMatrix


class TestUtils(unittest.TestCase):

    def test_logical_contour_point(self):
        self.assertEqual(CP(0, 0), CP(0, 0))
        self.assertNotEqual(CP(0, 0), CP(0, 1))
        self.assertNotEqual(CP(0, 0), CP(1, 0))
        self.assertNotEqual(CP(0, 0), None)

    def test_contour_point(self):
        self.assertNotEqual(CP(0, 0, True), CP(0, 0))
        self.assertNotEqual(CP(0, 0, False, True), CP(0, 0))

    def test_cpoint_flag(self):
        self.assertEqual(CP(0, 0).flag(contour.maxima), CP(0, 0, True))
        self.assertEqual(CP(0, 0).flag(contour.minima), CP(0, 0, False, True))
        self.assertEqual(CP(0, 0).flag('Both'), CP(0, 0, True, True))

    def test_cpoint_unflag(self):
        self.assertEqual(CP(0, 0, True).unflag(contour.maxima), CP(0, 0))
        self.assertEqual(CP(0, 0, True, True).unflag(contour.maxima), CP(0, 0, False, True))
        self.assertEqual(CP(0, 0, True, True).unflag(contour.minima), CP(0, 0, True, False))
        self.assertEqual(CP(0, 0, False, True).unflag(contour.minima), CP(0, 0, False, False))
        self.assertEqual(CP(0, 0, True, True).unflag('Both'), CP(0, 0, False, False))

    def test_logical_contour(self):
        self.assertNotEqual(Contour([0, 1, 2]), Contour([0, 1]))
        self.assertEqual(Contour([0, 1, 2]), Contour([0, 1, 2]))
        self.assertNotEqual(Contour([0, 1, 2]), Contour([0, 2, 1]))
        self.assertNotEqual(Contour([0, 1, 2]), None)

    def test_contour(self):
        self.assertEqual(Contour([CP(0, 0), CP(1, 1)]), Contour([0, 1]))

    def test_build_classes_card(self):
        fn = contour.build_classes_card
        result = [(4, 1, (0, 1, 2, 3), True), (4, 2, (0, 1, 3, 2), False),
                  (4, 3, (0, 2, 1, 3), True), (4, 4, (0, 2, 3, 1), False),
                  (4, 5, (0, 3, 1, 2), False), (4, 6, (0, 3, 2, 1), False),
                  (4, 7, (1, 0, 3, 2), True), (4, 8, (1, 3, 0, 2), True)]
        self.assertEqual(fn(4), result)

    def test_build_classes(self):
        fn = contour.build_classes
        result = [[(2, 1, (0, 1), True)],
                  [(3, 1, (0, 1, 2), True), (3, 2, (0, 2, 1), False)],
                  [(4, 1, (0, 1, 2, 3), True), (4, 2, (0, 1, 3, 2), False),
                   (4, 3, (0, 2, 1, 3), True), (4, 4, (0, 2, 3, 1), False),
                   (4, 5, (0, 3, 1, 2), False), (4, 6, (0, 3, 2, 1), False),
                   (4, 7, (1, 0, 3, 2), True), (4, 8, (1, 3, 0, 2), True)]]
        self.assertEqual(fn(4), result)

    def test_contour_class(self):
        self.assertEqual(contour.contour_class(6, 117), Contour([0, 5, 4, 2, 1, 3]))

    def test_subsets_grouped(self):
        n = {(0, 1, 3, 2): [[0, 1, 4, 2]],
             (0, 2, 1, 3): [[0, 3, 1, 4]],
             (0, 2, 3, 1): [[0, 3, 4, 2]],
             (0, 3, 1, 2): [[0, 3, 1, 2]],
             (1, 3, 0, 2): [[3, 1, 4, 2]]}
        result = 'Prime form < 0 1 3 2 > (1)\n< 0 1 4 2 >\n' + \
                 'Prime form < 0 2 1 3 > (1)\n< 0 3 1 4 >\n' + \
                 'Prime form < 0 2 3 1 > (1)\n< 0 3 4 2 >\n' + \
                 'Prime form < 0 3 1 2 > (1)\n< 0 3 1 2 >\n' + \
                 'Prime form < 1 3 0 2 > (1)\n< 3 1 4 2 >'
        self.assertEqual(contour.subsets_grouped(n, "prime"), result)

    def test_rotation(self):
        self.assertEqual(Contour([1, 4, 9, 9, 2, 1]).rotation(), Contour([4, 9, 9, 2, 1, 1]))
        self.assertEqual(Contour([1, 4, 9, 9, 2, 1]).rotation(1), Contour([4, 9, 9, 2, 1, 1]))
        self.assertEqual(Contour([1, 4, 9, 9, 2, 1]).rotation(2), Contour([9, 9, 2, 1, 1, 4]))
        self.assertEqual(Contour([1, 4, 9, 9, 2, 1]).rotation(20), Contour([9, 9, 2, 1, 1, 4]))

    def test_retrogression(self):
        self.assertEqual(Contour([1, 4, 9, 9, 2, 1]).retrogression(), Contour([1, 2, 9, 9, 4, 1]))

    def test_inversion(self):
        self.assertEqual(Contour([1, 4, 9, 9, 2, 1]).inversion(), Contour([8, 5, 0, 0, 7, 8]))

    def test_translation(self):
        self.assertEqual(Contour([1, 4, 9, 9, 2, 1]).translation(), Contour([0, 2, 3, 3, 1, 0]))

    def test_cpoint(self):
        self.assertEqual(Contour([1, 4, 9, 9, 2, 1]).cpoint(2), CP(2, 9))

    def test_repetition_cpitch_test(self):
        self.assertEqual(Contour([0, 1, 0]).repetition_cpitch_test(), False)
        self.assertEqual(Contour([0, 1, 1, 0]).repetition_cpitch_test(), False)
        self.assertEqual(Contour([0, 1, 2]).repetition_cpitch_test(), True)

    def test_remove_repeated_adjacent_cps(self):
        self.assertEqual(Contour([0, 1, 1, 0]).remove_repeated_adjacent_cps(), Contour([CP(0, 0), CP(1, 1), CP(3, 0)]))
        self.assertEqual(Contour([0, 1, 1, 0]).remove_repeated_adjacent_cps(False), [CP(0, 0), CP(1, 1), CP(3, 0)])
        self.assertEqual(Contour([0, 2, 1, 1]).remove_repeated_adjacent_cps(False, True), [CP(0, 0), CP(1, 2), CP(3, 1)])

    def test_prime_form_marvin_laprade(self):
        cseg01, cseg02 = Contour([1, 4, 9, 2]), Contour([0, 2, 3, 1])
        cseg03, cseg04 = Contour([5, 7, 9, 1]), Contour([0, 3, 2, 1])
        cseg05 = Contour([0, 2, 1, 3, 4])
        cseg06 = Contour([0, 1, 2, 3, 2])
        cseg07, cseg08 = Contour([0, 1, 2, 4, 3]), Contour([0, 1, 3, 4, 2])
        cseg09 = Contour([1, 2, 3, 0, 3, 1])
        cseg10, cseg11 = [Contour([1, 3, 4, 0, 5, 2]), Contour([1, 4, 0, 5, 3, 2])]
        cseg12 = Contour([0, 1, 2, 1, 2])
        cseg13, cseg14 = [Contour([0, 1, 3, 2, 4]), Contour([0, 2, 4, 1, 3])]
        self.assertEqual(cseg01.prime_form_marvin_laprade(), cseg02)
        self.assertEqual(cseg03.prime_form_marvin_laprade(), cseg04)
        self.assertEqual(cseg05.prime_form_marvin_laprade(), cseg05)
        self.assertEqual(cseg06.prime_form_marvin_laprade(), [cseg07, cseg08])
        self.assertEqual(cseg09.prime_form_marvin_laprade(), [cseg10, cseg11])
        self.assertEqual(cseg12.prime_form_marvin_laprade(), [cseg13, cseg14])

    def test_prime_form_sampaio(self):
        cseg1, cseg2 = Contour([1, 4, 9, 2]), Contour([0, 2, 3, 1])
        cseg3, cseg4 = Contour([5, 7, 9, 1]), Contour([0, 3, 2, 1])
        cseg5, cseg6 = Contour([0, 2, 1, 3, 4]), Contour([0, 1, 3, 2, 4])
        cseg7, cseg8 = Contour([0, 1, 2, 1, 2]), Contour([0, 2, 4, 1, 3])
        self.assertEqual(cseg1.prime_form_sampaio(), cseg2)
        self.assertEqual(cseg3.prime_form_sampaio(), cseg4)
        self.assertEqual(cseg5.prime_form_sampaio(), cseg6)
        self.assertEqual(cseg7.prime_form_sampaio(), [cseg6, cseg8])

    def test_unique_prime_form_test(self):
        cseg1 = Contour([0, 2, 1, 3, 4])
        algorithm1 = "prime_form_marvin_laprade"
        cseg2 = Contour([0, 2, 1, 3, 4])
        algorithm2 = "prime_form_sampaio"
        self.assertEqual(cseg1.unique_prime_form_test(algorithm1), False)
        self.assertEqual(cseg2.unique_prime_form_test(algorithm2), True)

    def test_subsets(self):
        cseg = Contour([2, 8, 12, 9])
        self.assertEqual(cseg.subsets(2), [Contour([2, 8]), Contour([2, 9]), Contour([2, 12]), Contour([8, 9]), Contour([8, 12]), Contour([12, 9])])
        self.assertEqual(cseg.subsets(3), [Contour([2, 8, 9]), Contour([2, 8, 12]), Contour([2, 12, 9]), Contour([8, 12, 9])])

    def test_subsets_prime(self):
        cseg = Contour([0, 3, 1, 4, 2])
        result = {(0, 1, 3, 2): [Contour([0, 1, 4, 2])],
                  (0, 2, 1, 3): [Contour([0, 3, 1, 4])],
                  (0, 2, 3, 1): [Contour([0, 3, 4, 2])],
                  (0, 3, 1, 2): [Contour([0, 3, 1, 2])],
                  (1, 3, 0, 2): [Contour([3, 1, 4, 2])]}
        self.assertEqual(cseg.subsets_prime(4), result)

    def test_subsets_normal(self):
        cseg1 = Contour([0, 3, 1, 4, 2])
        result1 = {(0, 1, 3, 2): [Contour([0, 1, 4, 2])],
                   (0, 2, 1, 3): [Contour([0, 3, 1, 4])],
                   (0, 2, 3, 1): [Contour([0, 3, 4, 2])],
                   (0, 3, 1, 2): [Contour([0, 3, 1, 2])],
                   (2, 0, 3, 1): [Contour([3, 1, 4, 2])]}
        cseg2 = Contour([0, 1, 2, 0])
        result2 = {(0, 1, 0): [Contour([0, 1, 0]), Contour([0, 2, 0])],
                   (0, 1, 2): [Contour([0, 1, 2])],
                   (1, 2, 0): [Contour([1, 2, 0])]}
        self.assertEqual(cseg1.subsets_normal(4), result1)
        self.assertEqual(cseg2.subsets_normal(3), result2)

    def test_all_subsets(self):
        cseg = Contour([2, 8, 12, 9])
        result = [Contour([2, 8]), Contour([2, 9]), Contour([2, 12]),
                  Contour([8, 9]), Contour([8, 12]), Contour([12, 9]),
                  Contour([2, 8, 9]), Contour([2, 8, 12]), Contour([2, 12, 9]),
                  Contour([8, 12, 9]), Contour([2, 8, 12, 9])]
        self.assertEqual(cseg.all_subsets(), result)

    def test_all_subsets_prime(self):
        cseg = Contour([2, 8, 12])
        result = {(0, 1): [Contour([2, 8]), Contour([2, 12]), Contour([8, 12])],
                  (0, 1, 2): [Contour([2, 8, 12])]}
        self.assertEqual(cseg.all_subsets_prime(), result)

    def test_all_subsets_normal(self):
        cseg1 = Contour([2, 8, 7])
        result1 = {(0, 1): [Contour([2, 7]), Contour([2, 8])],
                   (0, 2, 1): [Contour([2, 8, 7])],
                   (1, 0): [Contour([8, 7])]}
        cseg2 = Contour([2, 8, 2])
        result2 = {(0, 0): [Contour([2, 2])],
                   (0, 1): [Contour([2, 8])],
                   (0, 1, 0): [Contour([2, 8, 2])],
                   (1, 0): [Contour([8, 2])]}
        self.assertEqual(cseg1.all_subsets_normal(), result1)
        self.assertEqual(cseg2.all_subsets_normal(), result2)

    def test_subsets_adj(self):
        cseg = Contour([2, 8, 12, 9, 5, 7, 3, 12, 3, 7])
        result = [Contour([2, 8, 12, 9]), Contour([8, 12, 9, 5]), Contour([12, 9, 5, 7]),
                  Contour([9, 5, 7, 3]), Contour([5, 7, 3, 12]), Contour([7, 3, 12, 3]),
                  Contour([3, 12, 3, 7])]
        self.assertEqual(cseg.subsets_adj(4), result)

    def test_cpoint_replace(self):
        cp1 = CP(0, 0)
        cp2 = CP(1, 3)
        cseg = Contour([cp1, cp2])
        cp3 = CP(1, 3, True)
        self.assertEqual(cseg.cpoint_replace(cp2, cp3), Contour([cp1, cp3]))

    def test_cpoint_flag(self):
        self.assertEqual(Contour([CP(0, 0)]).cpoint_flag(CP(0, 0), contour.maxima), Contour([CP(0, 0, True)]))
        self.assertEqual(Contour([CP(0, 0)]).cpoint_flag(CP(0, 0), contour.minima), Contour([CP(0, 0, False, True)]))
        self.assertEqual(Contour([CP(0, 0)]).cpoint_flag(CP(0, 0), 'Both'), Contour([CP(0, 0, True, True)]))
        self.assertEqual(Contour([CP(0, 0, True)]).cpoint_flag(CP(0, 0, True), contour.maxima, True), Contour([CP(0, 0)]))
        self.assertEqual(Contour([CP(0, 0, False, True)]).cpoint_flag(CP(0, 0, False, True), contour.minima, True), Contour([CP(0, 0)]))
        self.assertEqual(Contour([CP(0, 0, True, True)]).cpoint_flag(CP(0, 0, True, True), 'Both', True), Contour([CP(0, 0)]))

    def test_max_min_flag(self):
        result = Contour([CP(0, 0, True, True), CP(1, 2, True), CP(2, 1, False, True), CP(3, 3, True, True)])
        self.assertEqual(Contour([0, 2, 1, 3]).max_min_flag(), result)

    def test_unflagged_remove(self):
        self.assertEqual(Contour([CP(0, 0, True), CP(1, 4)]).unflagged_remove(), Contour([CP(0, 0, True)]))

    def test_max_min_list(self):
        self.assertEqual(Contour([0, 3, 2, 1]).max_min_list(contour.maxima), [CP(0, 0), CP(1, 3), CP(3, 1)])

    def test_flag(self):
        cseg = Contour([0, 4, 3, 2, 5, 5, 1])
        result = ([CP(0, 0), CP(1, 4), CP(4, 5), CP(5, 5), CP(6, 1)],
                   [CP(0, 0), CP(3, 2), CP(6, 1)])
        self.assertEqual(cseg.flag(), result)

    def test_all_flagged(self):
        cseg = Contour([0, 4, 3, 2, 5, 5, 1])
        max_list = ([CP(0, 0), CP(1, 4), CP(4, 5), CP(5, 5),
                     CP(6, 1)])
        min_list = ([CP(0, 0), CP(3, 2), CP(6, 1)])
        result = (False, ([CP(0, 0), CP(1, 4), CP(4, 5), CP(5, 5), CP(6, 1)],
                          [CP(0, 0), CP(3, 2), CP(6, 1)]))
        self.assertEqual(cseg.all_flagged(max_list, min_list), result)

    def test_reduction_morris(self):
        cseg1, cseg2 = Contour([0, 4, 3, 2, 5, 5, 1]), Contour([0, 2, 1])
        cseg3, cseg4 = Contour([7, 10, 9, 0, 2, 3, 1, 8, 6, 2, 4, 5]), Contour([2, 3, 0, 1])
        self.assertEqual(cseg1.reduction_morris(), [cseg2, 2])
        self.assertEqual(cseg2.reduction_morris(), [cseg2, 0])
        self.assertEqual(cseg3.reduction_morris(), [cseg4, 3])

    def test_reduction_window(self):
        cseg1 = Contour([7, 10, 9, 0, 2, 3, 1, 8, 6, 2, 4, 5])
        cseg2 = Contour([7, 10, 0, 1, 8, 2, 5])
        cseg3 = Contour([7, 10, 0, 8, 5])
        cseg4 = Contour([7, 10, 0, 5])
        cseg5 = Contour([0, 3, 3, 1, 2, 4])
        cseg6 = Contour([0, 3, 1, 4])
        cseg7 = Contour([0, 3, 3, 1, 2])
        cseg8 = Contour([0, 3, 1, 2])
        cseg9 = Contour([12, 10, 13, 11, 7, 9, 8, 6, 3, 5, 4, 1, 0, 2])
        cseg10 = Contour([12, 10, 13, 7, 3, 0, 2])
        cseg11 = Contour([0, 2, 1, 3])
        cseg12 = Contour([0, 6, 1, 4, 3, 5, 2])
        self.assertEqual(cseg1.reduction_window(3, False), Contour([7, 10, 0, 3, 1, 8, 2, 5]))
        self.assertEqual(cseg1.reduction_window(3, True), Contour([5, 7, 0, 3, 1, 6, 2, 4]))
        self.assertEqual(cseg1.reduction_window(5, False), cseg2)
        self.assertEqual(cseg2.reduction_window(5, False), cseg3)
        self.assertEqual(cseg3.reduction_window(5, False), cseg4)
        self.assertEqual(cseg5.reduction_window(5, False), cseg6)
        self.assertEqual(cseg7.reduction_window(5, False), cseg8)
        self.assertEqual(cseg9.reduction_window(5, False), cseg10)
        self.assertEqual(cseg5.reduction_window(5, True), cseg11)
        self.assertEqual(cseg12.reduction_window(3, False), cseg12)

    def test_reduction_window_recursive(self):
        cseg1 = Contour([0, 3, 3, 1, 2])
        # FIXME: Improves contour example.
        cseg2 = Contour([0, 1, 1, 3, 2])
        cseg3 = Contour([7, 10, 9, 0, 2, 3, 1, 8, 6, 2, 4, 5])
        self.assertEqual(cseg1.reduction_window_recursive(3, False), [Contour([0, 3, 1, 2]), 1])
        self.assertEqual(cseg2.reduction_window_recursive(3, True), [Contour([0, 2, 1]), 2])
        self.assertEqual(cseg3.reduction_window_recursive(5, False), [Contour([7, 10, 0, 5]), 3])

    def test_reduction_bor(self):
        cseg1 = Contour([0, 6, 1, 4, 3, 5, 2])
        cseg2 = Contour([12, 10, 13, 11, 7, 9, 8, 6, 3, 5, 4, 1, 0, 2])
        cseg3 = Contour([7, 10, 9, 0, 2, 3, 1, 8, 6, 2, 4, 5])
        self.assertEqual(cseg1.reduction_bor(53), [Contour([0, 2, 1]), 2])
        self.assertEqual(cseg1.reduction_bor(35), [Contour([0, 3, 2, 1]), 1])
        self.assertEqual(cseg2.reduction_bor(53, False), [Contour([12, 10, 13, 0, 2]), 2])
        self.assertEqual(cseg3.reduction_bor(35, False), [Contour([7, 10, 0, 8, 5]), 2])
        self.assertEqual(cseg3.reduction_bor(35, True), [Contour([2, 4, 0, 3, 1]), 2])
        self.assertEqual(cseg2.reduction_bor(53, False), [Contour([12, 10, 13, 0, 2]), 2])
        self.assertEqual(cseg3.reduction_bor(355, False), [Contour([7, 10, 0, 5]), 3])
        self.assertEqual(cseg3.reduction_bor(555, True), [Contour([2, 3, 0, 1]), 3])

    def test_reduction_sampaio(self):
        cseg1 = Contour([0, 1, 0, 1, 0])
        cseg2 = Contour([1, 3, 0, 2, 1, 2, 1, 3, 0])
        self.assertEqual(cseg1.reduction_sampaio(), [Contour([0, 1, 0]), 1])
        self.assertEqual(cseg2.reduction_sampaio(), [Contour([1, 3, 0, 2, 1, 3, 0]), 1])

    def test_reduction_retention(self):
        self.assertEqual(contour.reduction_retention([CP(0, 0), CP(1, 0), CP(2, 0)]), None)
        self.assertEqual(contour.reduction_retention([CP(0, 0), CP(1, 0), CP(2, 1)]), None)
        self.assertEqual(contour.reduction_retention([CP(0, 1), CP(1, 1), CP(2, 0)]), None)
        self.assertEqual(contour.reduction_retention([CP(0, 0), CP(1, 1), CP(2, 0)]), CP(1, 1))
        self.assertEqual(contour.reduction_retention([CP(0, 1), CP(1, 0), CP(2, 1)]), CP(1, 0))
        self.assertEqual(contour.reduction_retention([CP(0, 1), CP(1, 0), CP(2, 0)]), CP(1, 0))
        self.assertEqual(contour.reduction_retention([CP(0, 0), CP(1, 1), CP(2, 1)]), CP(1, 1))
        self.assertEqual(contour.reduction_retention([CP(0, 0), CP(1, 2), CP(2, 1)]), CP(1, 2))
        self.assertEqual(contour.reduction_retention([None, CP(1, 0), CP(2, 0)]), CP(1, 0))
        self.assertEqual(contour.reduction_retention([None, CP(1, 0), CP(2, 1)]), CP(1, 0))
        self.assertEqual(contour.reduction_retention([None, CP(1, 1), CP(2, 0)]), CP(1, 1))
        self.assertEqual(contour.reduction_retention([None, CP(1, 1), CP(2, 2)]), CP(1, 1))
        self.assertEqual(contour.reduction_retention([CP(0, 0), CP(1, 0), None]), CP(1, 0))
        self.assertEqual(contour.reduction_retention([CP(0, 0), CP(1, 1), None]), CP(1, 1))
        self.assertEqual(contour.reduction_retention([CP(0, 1), CP(1, 0), None]), CP(1, 0))
        self.assertEqual(contour.reduction_retention([None, None, CP(2, 0), CP(3, 1), CP(4, 2)]), CP(2, 0))
        self.assertEqual(contour.reduction_retention([CP(0, 0), CP(1, 2), CP(2, 1), None, None]), CP(2, 1))
        self.assertEqual(contour.reduction_retention([None, CP(1, 7), CP(2, 10), CP(3, 9), CP(4, 0)]), CP(2, 10))
        self.assertEqual(contour.reduction_retention([CP(0, 7), CP(1, 10), CP(2, 9), CP(3, 0), CP(4, 2)]), None)
        self.assertEqual(contour.reduction_retention([CP(0, 0), CP(1, 2), CP(2, 1), CP(3, 4), CP(4, 1)]), None)
        self.assertEqual(contour.reduction_retention([CP(0, 1), CP(1, 4), CP(2, 1), CP(3, 5), CP(4, 3)]), CP(2, 1))
        self.assertEqual(contour.reduction_retention([CP(0, 3), CP(1, 0), CP(2, 4), CP(3, 1), CP(4, 4)]), CP(2, 4))
        self.assertEqual(contour.reduction_retention([CP(0, 4), CP(1, 1), CP(2, 4), CP(3, 3), CP(4, 5)]), None)
        self.assertEqual(contour.reduction_retention([CP(0, 1), CP(1, 0), CP(2, 5), CP(3, 2), CP(4, 5)]), CP(2, 5))
        self.assertEqual(contour.reduction_retention([CP(0, 5), CP(1, 2), CP(2, 5), CP(3, 3), CP(4, 4)]), CP(2, 5))
        self.assertEqual(contour.reduction_retention([CP(0, 0), CP(1, 3), CP(2, 2), CP(3, 4), CP(4, 2)]), None)
        self.assertEqual(contour.reduction_retention([CP(0, 2), CP(1, 4), CP(2, 2), CP(3, 5), CP(4, 1)]), None)

    def test_contour_rotation_classes(self):
        result = [Contour([0, 1, 2, 3]), Contour([0, 1, 3, 2]), Contour([0, 2, 1, 3])]
        self.assertEqual(contour.contour_rotation_classes(4), result)

    def test_interval_succession(self):
        self.assertEqual(Contour([0, 1, 3, 2]).interval_succession(), [1, 2, -1])

    def test_absolute_intervals_sum(self):
        self.assertEqual(Contour([0, 1, 3, 2]).absolute_intervals_sum(), 4)

    def test_absolute_intervals_average(self):
        self.assertEqual(Contour([0, 1, 2, 3]).absolute_intervals_average(), 0.75)

    def test_absolute_intervals_index(self):
        self.assertEqual(Contour([0, 1, 2, 3]).absolute_intervals_index(), 0.42857142857142855)

    def test_internal_diagonals(self):
        cseg1 = Contour([0, 2, 3, 1])
        cseg2 = Contour([1, 0, 4, 3, 2])
        self.assertEqual(cseg1.internal_diagonals(1), InternalDiagonal([1, 1, -1]))
        self.assertEqual(cseg1.internal_diagonals(2), InternalDiagonal([1, -1]))
        self.assertEqual(cseg2.internal_diagonals(1), InternalDiagonal([-1, 1, -1, -1]))
        self.assertEqual(cseg2.internal_diagonals(2), InternalDiagonal([1, 1, -1]))

    def test_interval_succession(self):
        cseg = Contour([0, 1, 3, 2])
        self.assertEqual(cseg.interval_succession(), [1, 2, -1])

    def test_comparison_matrix(self):
        cseg1 = Contour([0, 2, 3, 1])
        cseg2 = Contour([1, 2, 3, 0, 3, 1])
        result1 = ComparisonMatrix([[0, 1, 1, 1], [-1, 0, 1, -1], [-1, -1, 0, -1], [-1, 1, 1, 0]])
        result2 = ComparisonMatrix([[0, 1, 1, -1, 1, 0], [-1, 0, 1, -1, 1, -1], [-1, -1, 0, -1, 0, -1],
                                    [1, 1, 1, 0, 1, 1], [-1, -1, 0, -1, 0, -1], [0, 1, 1, -1, 1, 0]])
        self.assertEqual(cseg1.comparison_matrix(), result1)
        self.assertEqual(cseg2.comparison_matrix(), result2)

    def test_fuzzy_membership_matrix(self):
        cseg1 = Contour([0, 2, 3, 1])
        cseg2 = Contour([1, 2, 3, 0, 3, 1])
        result1 = FuzzyMatrix([[0, 1, 1, 1],
                               [0, 0, 1, 0],
                               [0, 0, 0, 0],
                               [0, 1, 1, 0]])
        result2 = FuzzyMatrix([[0, 1, 1, 0, 1, 0],
                               [0, 0, 1, 0, 1, 0],
                               [0, 0, 0, 0, 0, 0],
                               [1, 1, 1, 0, 1, 1],
                               [0, 0, 0, 0, 0, 0],
                               [0, 1, 1, 0, 1, 0]])
        self.assertEqual(cseg1.fuzzy_membership_matrix(), result1)
        self.assertEqual(cseg2.fuzzy_membership_matrix(), result2)

    def test_fuzzy_comparison_matrix(self):
        cseg1 = Contour([0, 2, 3, 1])
        cseg2 = Contour([1, 2, 3, 0, 3, 1])
        result1 = FuzzyMatrix([[0, 1, 1, 1], [-1, 0, 1, -1], [-1, -1, 0, -1], [-1, 1, 1, 0]])
        result2 =  FuzzyMatrix([[0, 1, 1, -1, 1, 0],
                                [-1, 0, 1, -1, 1, -1],
                                [-1, -1, 0, -1, 0, -1],
                                [1, 1, 1, 0, 1, 1],
                                [-1, -1, 0, -1, 0, -1],
                                [0, 1, 1, -1, 1, 0]])
        self.assertEqual(cseg1.fuzzy_comparison_matrix(), result1)
        self.assertEqual(cseg2.fuzzy_comparison_matrix(), result2)

    def test_adjacency_series_vector(self):
        self.assertEqual(Contour([0, 2, 3, 1]).adjacency_series_vector(), [2, 1])
        self.assertEqual(Contour([1, 2, 3, 0, 3, 1]).adjacency_series_vector(), [3, 2])

    def test_interval_array(self):
        self.assertEqual(Contour([0, 1, 3, 2]).interval_array(), ([2, 2, 1], [1, 0, 0]))

    def test_class_vector_i(self):
        self.assertEqual(Contour([0, 1, 3, 2]).class_vector_i(), [9, 1])

    def test_class_vector_ii(self):
        self.assertEqual(Contour([0, 1, 3, 2]).class_vector_ii(), [5, 1])

    def test_class_index_i(self):
        self.assertEqual(Contour([0, 1, 3, 2]).class_index_i(), 0.9)

    def test_class_index_ii(self):
        self.assertEqual(Contour([0, 1, 3, 2]).class_index_ii(), 5.0 / 6)

    def test_segment_class(self):
        self.assertEqual(Contour([2, 1, 4]).segment_class(), (3, 2, Contour([0, 2, 1]), False))
        self.assertEqual(Contour([3, 1, 0]).segment_class(), (3, 1, Contour([0, 1, 2]), True))

    def test_ri_identity_test(self):
        self.assertEqual(Contour([0, 1, 3, 2]).ri_identity_test(), False)
        self.assertEqual(Contour([1, 0, 3, 2]).ri_identity_test(), True)

    def test_symmetry_index(self):
        self.assertEqual(Contour([1, 0, 3, 2]).symmetry_index(), 1)
        self.assertEqual(Contour([0, 2, 1]).symmetry_index(), 0)
        self.assertEqual(Contour([0, 1, 3, 4, 2, 5, 6]).symmetry_index(), 0.5)

    def test_class_representatives(self):
        cseg = Contour([0, 1, 3, 2])
        result = [cseg, Contour([3, 2, 0, 1]), Contour([2, 3, 1, 0]), Contour([1, 0, 2, 3])]
        self.assertEqual(cseg.class_representatives(), result)

    def test_class_four_forms(self):
        cseg = Contour([0, 1, 3, 2])
        result = [cseg, Contour([3, 2, 0, 1]), Contour([2, 3, 1, 0]), Contour([1, 0, 2, 3])]
        self.assertEqual(cseg.class_four_forms(), result)

    def test_all_rotations(self):
        cseg1 = Contour([0, 1, 2])
        cseg2 = Contour([0, 3, 1, 2])
        result1 = [cseg1, Contour([1, 2, 0]), Contour([2, 0, 1]), Contour([0, 1, 2])]
        result2 = [cseg2, Contour([3, 1, 2, 0]), Contour([1, 2, 0, 3]),
                   Contour([2, 0, 3, 1]), Contour([0, 3, 1, 2])]
        self.assertEqual(cseg1.all_rotations(), result1)
        self.assertEqual(cseg2.all_rotations(), result2)

    def test_rotated_representatives(self):
        cseg1 = Contour([0, 1, 2])
        cseg2 = Contour([0, 3, 1, 2])
        result1 = [cseg1, Contour([0, 2, 1]), Contour([1, 0, 2]), Contour([1, 2, 0]),
                   Contour([2, 0, 1]), Contour([2, 1, 0])]
        result2 = [Contour([0, 2, 1, 3]), cseg2, Contour([1, 2, 0, 3]), Contour([1, 3, 0, 2]),
                   Contour([2, 0, 3, 1]), Contour([2, 1, 3, 0]), Contour([3, 0, 2, 1]),
                   Contour([3, 1, 2, 0])]
        self.assertEqual(cseg1.rotated_representatives(), result1)
        self.assertEqual(cseg2.rotated_representatives(), result2)

    def test_oscillation(self):
        self.assertEqual(Contour([0, 1]).oscillation(), 0)
        self.assertEqual(Contour([0, 1, 0]).oscillation(), 1)
        self.assertEqual(Contour([0, 1, 0, 2]).oscillation(), 2)

    def test_oscillation_index(self):
        self.assertEqual(Contour([0, 1]).oscillation_index(), 0)
        self.assertEqual(Contour([0, 1, 0]).oscillation_index(), 0.5)
        self.assertEqual(Contour([0, 1, 0, 2, 0]).oscillation_index(), 0.75)
        self.assertEqual(Contour([0, 1, 2, 3, 0]).oscillation_index(), 0.25)

    def test_prime_form_algorithm_test(self):
        algorithm1 = "prime_form_marvin_laprade"
        algorithm2 = "prime_form_sampaio"
        result = [[(5, 3), Contour([0, 1, 3, 2, 4]), Contour([0, 2, 1, 3, 4])],
                   [(5, 8), Contour([0, 2, 3, 1, 4]), Contour([0, 3, 1, 2, 4])],
                   [(5, 25), Contour([1, 0, 4, 2, 3]), Contour([1, 2, 0, 4, 3])],
                   [(5, 27), Contour([1, 2, 4, 0, 3]), Contour([1, 4, 0, 2, 3])]]
        self.assertEqual(contour.prime_form_algorithm_test(4, algorithm1), [])
        self.assertEqual(contour.prime_form_algorithm_test(5, algorithm1), result)
        self.assertEqual(contour.prime_form_algorithm_test(6, algorithm2), [])

    def test_base_three_representation(self):
        self.assertEqual(Contour([0, 1]).base_three_representation(), [[2]])
        self.assertEqual(Contour([1, 0]).base_three_representation(), [[0]])
        self.assertEqual(Contour([0, 1, 0]).base_three_representation(), [[2, 1], [0]])
        self.assertEqual(Contour([0, 1, 2]).base_three_representation(), [[2, 2], [2]])
        self.assertEqual(Contour([0, 2, 1]).base_three_representation(), [[2, 2], [0]])

    def test_possible_cseg(self):
        self.assertEqual(contour.possible_cseg([[2, 2], [2]]), Contour([0, 1, 2]))
        self.assertEqual(contour.possible_cseg([[0, 2], [1]]), "Impossible cseg")

if __name__ == '__main__':
    unittest.main()
