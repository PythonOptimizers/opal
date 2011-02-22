============
Installation
============

OPAL is provided as Python package and can be easily installed by built-in utility `distutil`. To make OPAL work, some
minimum requirements need to be prepared.

Requirements
============

Python 2.6 is crtical required. The previous version may result in some errors relating to the `import` statement. The
Python 3.0 has huge change on the syntax, and OPAL is not tested with this change.

OPAL use NOMAD as default solver, installation of NOMAD is not need to install OPAL but it is needed to run the simplest
examples provided in the package. NOMAD can be downloaded at `<http://www.gerad.ca/NOMAD>`_.

Sphinx documentation sytem `<http://sphinx.pocoo.org>`_.

Download and instalation
========================

After getting the package in form of gzip package, for example ``opal-1.0.tar.gz``, uncompress it and all of the
package is in the directory ``opal-1.0``. Follow the instruction in ``installation.txt`` to install the package. In the
simplest case, the installation is done by only command::

  shell$ python setup.py install

Documentation
=============

This document is can rebuilt from the source file and installed package by Sphinx. Suppose that the OPAL and Sphinx
is installed. The documentation is built by::

  shell$ cd doc/reference
  shell$ make html

You will get a `build` directory at current working directory that contains all to show the documentation as html pages.


