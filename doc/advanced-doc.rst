Advanced documentation
======================

This documentation is designed to users that are familiar to command
line. MusiContour has many features available only in Python
environment.

Install
-------

We recommend to install directly from repository. The tarballs are
only to install specific versions of MusiContour.

Directly from repository
~~~~~~~~~~~~~~~~~~~~~~~~

Be sure that `Git <http://git-scm.com/>`_ is installed and clone the
repo::

 git clone https://msampaio@github.com/msampaio/MusiContour.git

To use the development version, inside MusiContour directory, run::

 git branch --track development origin/development
 git checkout development

From a tarball
~~~~~~~~~~~~~~

Download tarball in
https://github.com/msampaio/MusiContour/tarball/master and unpack
it. For example::

 tar xf msampaio-MusiContour-0.2-60-gbaba48c.tar.gz

Rename directory to MusiContour::

 mv msampaio-MusiContour-0.2-60-gbaba48c MusiContour


Installing dependencies
-----------------------

This tutorial is for Mac and Linux only.

Virtualenv
~~~~~~~~~~

The best way to use MusiContour is with `Virtualenv
<https://pypi.python.org/pypi/virtualenv>`_. Virtualenv allows
isolated instances of Python and is useful to test different versions
of libraries.

To install pip, virtualenv, and virtualenvwrapper run::

 easy_install pip
 pip install virtualenv virtualenvwrapper

We recommend to make a directory `~/.virtualenvs` and to insert these
lines in `~/.bashrc`::

 export VIRTUALENVWRAPPER_VIRTUALENV_ARGS='--no-site-packages --distribute'
 export WORKON_HOME=~/.virtualenvs
 source /usr/local/bin/virtualenvwrapper.sh
 export PIP_VIRTUALENV_BASE=$WORKON_HOME
 export PIP_RESPECT_VIRTUALENV=true

Make a new virtualenv with this command::

 mkvirtualenv MusiContour

Use this command to run the MusiContour virtualenv::

 workon MusiContour

Use this command to quit virtualenv::

 deactivate

Once running the virtualenv, and inside `MusiContour` downloaded
directory, install these dependencies::

 pip install numpy
 pip install -r requirements.txt

Maybe you have to install readline in virtualenv::

 easy_install readline

Install MusiContour in virtualenv::

 python setup.py install
 
Music21 and MuseScore/Finale
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The `contour.composition` packages requires `Music21
<http://web.mit.edu/music21/>`_ and `MuseScore
<http://musescore.org/>`_. MuseScore can be substituted by Finale. The
MuseScore can be installed directly from its website, and the Music21
has a `tutorial to install
<http://web.mit.edu/music21/doc/html/install.html#install>`_.

Running
-------

Look at `MusiContour cheat sheet <cheat-sheet.html>`_
