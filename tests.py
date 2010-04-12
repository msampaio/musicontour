#!/usr/bin/env python
# -*- coding: utf-8 -*-

import contour as c
import subprocess

### data

## chorales

files = [str(n).zfill(3) for n in range(1, 371)]

files.remove("150")

freq_files = [n + '.freq' for n in files]

krn_files = [n + '.krn' for n in files]

## paths

krn_path = "/home/marcos/repositorios/genos-corpus/music/bach-chorales/kern/"

freq_path = "/tmp/freq-old/"

## extracting spines
# in one file:

c.kern_file_process(krn_path, "100", "*Ibass")

## in many files:

[c.kern_file_process(krn_path, f, "*Ibass") for f in files]


## running in one file

contour_class = c.contour_class_file(freq_path, "100.freq")

print(contour_class)

contour_class_comparison = c.frequency_file_contour_count(freq_path, "100.freq", 4)

print(contour_class_comparison)

c.lists_printing(c.percent(contour_class_comparison[2]))

## running in many files

x = c.count_contours_list_of_files(freq_path, freq_files, 3)

c.lists_printing(c.percent(x))
