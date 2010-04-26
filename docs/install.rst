Install
=======

Getting software
----------------

Villa Lobos Contour Module source code and user releases tarballs are
available.

User releases
~~~~~~~~~~~~~

The Linux users can download releases tarballs at
http://genos.mus.br/villa-lobos/download.

Linux users
```````````

Linux users must install also this dependency::

 sudo apt-get install python-matplotlib

Windows users
`````````````

Windows users must install `Python 2.6
<http://www.python.org/download/windows/>`_, `Numpy
<http://sourceforge.net/projects/numpy/>`_ and `Matplotlib
<http://matplotlib.sourceforge.net/>`_.

Maybe after install it's necessary to associate gui.py filetype to
Python2.6. In the example, in the picture, Python is in::

 C:\Python26\pythonw.exe

Look at the the picture:

.. figure:: figs/villa-lobos-windows-install.png

Mac users
`````````

VLCM was not tested in Macintosh, but probably can be installed
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
 sudo easy_install nose
 sudo easy_install pep8
 sudo easy_install pylint

Running
-------

To run Villa Lobos Contour Module GUI you have to open a terminal,
change to contour-module directory, and run one of these commands::

 python gui.py

or::

 ./gui.py
