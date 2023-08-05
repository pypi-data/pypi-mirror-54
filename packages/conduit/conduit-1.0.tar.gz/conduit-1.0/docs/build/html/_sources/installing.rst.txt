.. -*- mode: rst -*-

Installation
============

Conduit is a pure Python package that has a few dependencies for analytics such as NumPy and Pandas as well as connecting to a BTrDB database. Conduit is intended to be part of an analytics suite that includes SciPy, Jupyter notebooks, matplotlib and more.

Installing with pip
-------------------

We recommend using ``pip`` to install conduit on all platforms::

    $ pip install conduit

To get a specific version of conduit, supply a version number. E.g.::

    $  pip install conduit==1.0

To upgrade to the latest version of conduit::

    $ pip install --upgrade conduit

Installing with Anaconda
------------------------

If you'd like to use Anaconda, you can use ``conda`` to install the package from the PingThings channel as shown below::

    $ conda install -c pingthings conduit
