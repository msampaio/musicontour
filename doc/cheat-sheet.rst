MusiContour Cheat sheet
=======================

1. Open Python interpreter::

        $ python
        Python 2.6.6 (r266:84292, Sep 15 2010, 15:52:39)
        [GCC 4.4.5] on linux2
        Type "help", "copyright", "credits" or "license" for more information.
        >>>

2. Import desired packages::

          >>> import contour.contour as contour
          >>> import contour.comparison as comparison
          >>> import contour.auxiliary as auxiliary
          >>> import contour.plot as plot

3. Abstract a contour into a variable::

            >>> foo = contour.Contour([1, 0, 3, 2])
            >>> foo
            < 1 0 3 2 >

4. Contour methods::

           >>> foo.inversion()
           < 2 3 0 1 >

           >>> foo.internal_diagonals()
           < - + - >

           >>> foo.comparison_matrix()
             | 1 0 3 2
           -----------
           1 | 0 - + +
           0 | + 0 + +
           3 | - - 0 -
           2 | - - + 0

5. Plot contour::

        >>> plot.contour_lines([cseg, 'blue', 'legend'])

6. Help on methods (q to quit)::

        >>> help(foo.reduction_morris)
        Help on method reduction_morris in module contour.contour:

        reduction_morris(self) method of contour.contour.Contour instance
            Returns Morris (1993) contour reduction from a cseg, and
            its depth.

            >>> Contour([0, 4, 3, 2, 5, 5, 1]).reduction_morris()
            [< 0 2 1 >, 2]
