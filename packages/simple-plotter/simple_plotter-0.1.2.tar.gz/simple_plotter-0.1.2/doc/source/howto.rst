Getting started
===============

simple_plotter is a code-generator and minimal GUI frontend for plotting functional 2D x,y-plots.
The function equation has to be entered in python syntax (allowing the use of numpy statements).

Besides saving and loading projects to/from a JSON file, simple_plotter also provides the possibility to export the
project as python code.

.. image:: example.png

simple_plotter is released under GPLv3.

How to install
--------------

simple_plotter can either installed via pip or conda.

For pip use:

::

    TBD

or for conda:

::

    TBD

Requirements
------------
simple_plotter is written in python3 and requires following packages:

* pyqt >= 5
* jsonpickle
* numpy
* matplotlib
* setuptools_scm

Usage
-----

To launch simple_plotter just call

::

    python -m simple_plotter.gui

For detailed usage instructions see the :ref:`userguide`.


Developer information
---------------------

The source code can be obtained from:

https://gitlab.com/thecker/simple-plotter

For code documentation see the :ref:`apiRef`.
