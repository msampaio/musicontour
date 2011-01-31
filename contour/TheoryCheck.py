#!/usr/bin/env python
# -*- coding: utf-8 -*-

## This file has Contour Theory checking tests

from __future__ import print_function
import itertools
import contour
import comparison


## double prime form according to Marvin and Laprade prime form algorithm
double_pf = [contour.Contour([0, 2, 1, 3, 4]),
             contour.Contour([0, 3, 1, 2, 4]),
             contour.Contour([1, 2, 0, 4, 3]),
             contour.Contour([1, 4, 0, 2, 3]),
             contour.Contour([0, 2, 1, 3, 4, 5]),
             contour.Contour([0, 2, 3, 1, 4, 5]),
             contour.Contour([0, 3, 1, 2, 4, 5]),
             contour.Contour([0, 3, 2, 1, 4, 5]),
             contour.Contour([0, 4, 1, 2, 3, 5]),
             contour.Contour([0, 4, 1, 3, 2, 5]),
             contour.Contour([0, 4, 2, 1, 3, 5]),
             contour.Contour([0, 4, 3, 1, 2, 5]),
             contour.Contour([1, 2, 0, 3, 5, 4]),
             contour.Contour([1, 2, 3, 0, 5, 4]),
             contour.Contour([1, 3, 0, 2, 5, 4]),
             contour.Contour([1, 3, 2, 0, 5, 4]),
             contour.Contour([1, 5, 0, 2, 3, 4]),
             contour.Contour([1, 5, 0, 3, 2, 4]),
             contour.Contour([1, 5, 2, 0, 3, 4]),
             contour.Contour([1, 5, 3, 0, 2, 4]),
             contour.Contour([2, 1, 0, 4, 5, 3]),
             contour.Contour([2, 1, 4, 0, 5, 3]),
             contour.Contour([2, 4, 0, 1, 5, 3]),
             contour.Contour([2, 4, 1, 0, 5, 3]),
             contour.Contour([2, 5, 0, 1, 4, 3]),
             contour.Contour([2, 5, 0, 4, 1, 3]),
             contour.Contour([2, 5, 1, 0, 4, 3]),
             contour.Contour([2, 5, 4, 0, 1, 3])]


representatives_double_pf = [x.class_representatives() for x in double_pf]


def save_double_pf(filename, representatives):
    """Returns a list with cseg classes with double forms in Marvin
    and Laprade table."""

    with open(filename, "w") as f:
        f.write("Csegs classes with double prime forms in Marvin and Laprade table")
        f.write("\n")
        f.write("-" * 78)
        f.write("\n")
        f.write("{0:20} {1:20} {2:20} {3:20}".format("P", "IP", "RP", "RIP"))
        f.write("\n")
        f.write("-" * 78)
        f.write("\n")
        for [P, IP, RP, RIP] in representatives:
            f.write("{0:20} {1:20} {2:20} {3:20}\n".format(P, IP, RP, RIP))
