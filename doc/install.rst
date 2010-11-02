Install
=======

.. index:: Getting MusiContour

Getting software
----------------

MusiContour source code and user releases tarballs are
available.

User releases
~~~~~~~~~~~~~

MusiContour can be downloaded as tarballs or zipfiles at
http://github.com/mdsmus/MusiContour/archives/master

Linux users
```````````

Linux users must install also this dependency::

 sudo apt-get install python-tk python-matplotlib

Windows users
`````````````

Windows users must install manually all dependencies for MusiContour:
`Python 2.6 <http://www.python.org/download/windows/>`_, `Numpy
<http://sourceforge.net/projects/numpy/>`_, `Matplotlib
<http://matplotlib.sourceforge.net/>`_ and `PIL
<http://www.pythonware.com/products/pil/>`_.

Maybe after install it's necessary to associate gui.py filetype to
Python2.6. In the example, in the picture, Python is in::

 C:\Python26\pythonw.exe

Look at the the picture:

.. figure:: figs/villa-lobos-windows-install.png

Mac users
`````````

MusiContour was not tested in Macintosh, but probably can be installed
following `Windows users`_ steps.

Source code
~~~~~~~~~~~

The source code is available in
http://github.com/mdsmus/contour-module. It's possible to download a
package in http://github.com/mdsmus/contour-module/archives/master, or
to clone the repository::

 git clone git://github.com/mdsmus/contour-module.git

It's necessary to install these dependencies::

 sudo apt-get install python-setuptools python-matplotlib
 sudo apt-get install python-codespeak-lib
 sudo easy_install pep8
 sudo easy_install pylint

.. index:: Running MusiContour

Running
-------

On Linux
~~~~~~~~

To run MusiContour GUI in Linux you have to open a
terminal, change to contour-module directory, and run one of these
commands::

 python gui.py

or::

 ./gui.py

On Windows
~~~~~~~~~~

To run MusiContour GUI in Windows, double-click gui.py
file.
