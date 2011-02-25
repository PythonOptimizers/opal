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

In the case that you have no right of writing to the standard ``site-packages`` 
directory, a local ``site-packages`` has to be provided in installation command. 
  
  shell$ python setup.py install --prefix=$LOCAL_PYTHON_DIR

and the package shall be installed in ``$LOCAL_PYTHON_DIR/lib/python-2.6/site-packages`` 
(assume that the Python working version is 2.6) 

Documentation
=============

This document is can rebuilt from the source file and installed package by Sphinx. Suppose that the OPAL and Sphinx
is installed. The documentation is built by::

  shell$ cd doc/reference
  shell$ make html

You will get a `build` directory at current working directory that contains all to show the documentation as html pages.


