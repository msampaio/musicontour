#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from itertools import permutations

def permut_csegs(cardinality):
    """Returns a list of possible normalized csegs of a given
    cardinality."""

    base = range(cardinality)
    permutations(base, cardinality)
    return sorted(permutations(base, cardinality))
