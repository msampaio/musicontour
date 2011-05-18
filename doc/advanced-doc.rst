Advanced documentation
======================

This documentation is designed to users that are familiar to command
line. MusiContour has many features available only in Python
environment.

Install
-------

Directly from repository
~~~~~~~~~~~~~~~~~~~~~~~~

Be sure that `Git <http://git-scm.com/>`_ is installed and clone the
repo::

   git clone https://mdsmus@github.com/mdsmus/MusiContour.git

From a tarball
~~~~~~~~~~~~~~

Download tarball in
https://github.com/mdsmus/MusiContour/tarball/master and unpack
it. For example::

    tar xf mdsmus-MusiContour-0.2-60-gbaba48c.tar.gz

Rename directory to MusiContour::

       mv mdsmus-MusiContour-0.2-60-gbaba48c MusiContour


Installing dependencies
-----------------------

Linux users
~~~~~~~~~~~

Linux users must install also this dependency::

 sudo apt-get install python-tk python-matplotlib

`Music21 <http://web.mit.edu/music21/>`_ and `MuseScore
<http://musescore.org/>`_ are required to use contour.composition
package.

MuseScore can be installed with apt-get::

 sudo apt-get install musescore

Music21 has a `tutorial to install <http://web.mit.edu/music21/doc/html/install.html#install>`_.

Windows users
~~~~~~~~~~~~~

Windows users must install manually all dependencies for MusiContour:
`Python 2.6 <http://www.python.org/download/windows/>`_, `Numpy
<http://sourceforge.net/projects/numpy/>`_, `Matplotlib
<http://matplotlib.sourceforge.net/>`_ and `PIL
<http://www.pythonware.com/products/pil/>`_.

`Music21 <http://web.mit.edu/music21/>`_ and `MuseScore
<http://musescore.org/>`_ are required to use contour.composition
package.

Configuring
-----------

Linux users
~~~~~~~~~~~

Include MusiContour (and Music21) path in your PYTHONPATH environment
variable. Edit your ~/.bashrc (or ~/.zshrc) and include this line::

     export PYTHONPATH=$PATH:.:complete-path-to/MusiContour/:complete-path-to/music21/

Use absolute paths: /home/marcos/MusiContour instead of ~/MusiContour,
/home/marcos/music21 instead of ~/music21.

Running
-------

1. Open Python interpreter::

        $ python
        Python 2.6.6 (r266:84292, Sep 15 2010, 15:52:39)
        [GCC 4.4.5] on linux2
        Type "help", "copyright", "credits" or "license" for more information.
        >>>

2. Import desired packages::

          >>> import contour.contour
          >>> import contour.comparison
          >>> import contour.auxiliary
          >>> import contour.plot

3. Abstract a contour into a variable::

            >>> foo = contour.contour.Contour([1, 0, 3, 2])
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

        >>> contour.plot.contour_lines([cseg, "k", ""])

6. Help on methods (q to quit)::

        >>> help(foo.reduction_morris)
        Help on method reduction_morris in module contour.contour:

        reduction_morris(self) method of contour.contour.Contour instance
            Returns Morris (1993) contour reduction from a cseg, and
            its depth.

            >>> Contour([0, 4, 3, 2, 5, 5, 1]).reduction_morris()
            [< 0 2 1 >, 2]
