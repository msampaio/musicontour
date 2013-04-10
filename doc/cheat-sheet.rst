MusiContour Cheat sheet
=======================

1. Open Python interpreter::

        $ ipython

        Python 2.7.2 (default, Oct 11 2012, 20:14:37)
        Type "copyright", "credits" or "license" for more information.

        IPython 0.13.1 -- An enhanced Interactive Python.
        ?         -> Introduction and overview of IPython's features.
        %quickref -> Quick reference.
        help      -> Python's own help system.
        object?   -> Details about 'object', use 'object??' for extra details.

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
