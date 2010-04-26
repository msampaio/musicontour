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

Linux users must install also this dependency::

 sudo apt-get install python-matplotlib


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
