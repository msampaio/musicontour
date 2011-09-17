#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='MusiContour',
    version='0.3.1',
    author='Marcos da Silva Sampaio',
    author_email='marcos@sampaio.me',
    packages=['contour'],
    url='http://pypi.python.org/pypi/MusiContour/',
    license='COPYING',
    description='This app calculates and plot musical contour operations.',
    long_description=open('README').read(),
    platforms='Linux',
    install_requires=[
        "matplotlib >= 1.0.1",
        "music21 >= 0.3.7.a11"
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Operating System :: POSIX',
        'Programming Language :: Python'
    ],
)
