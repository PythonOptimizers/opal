============
Installation
============

OPAL is a Python package and can be easily installed with
`distutils`.

Requirements
============

Python version 2.6 or later is required. Previous versions may result in errors
relating to the `import` statement. OPAL was not tested with Python 3k.

OPAL use NOMAD as default solver. A working NOMAD installation is not needed to
install OPAL but is needed to run the simplest examples provided in the
package. NOMAD can be downloaded from `<http://www.gerad.ca/NOMAD>`_.

`Sphinx <http://sphinx.pocoo.org>`_ if you intend to rebuild the documentation.

Download and installation
=========================

After downloading
``opal-1.0.tar.gz``, uncompress it in the directory
``opal-1.0``. Follow the instruction in ``installation.txt`` to install the
package. In the simplest case, the installation requires only::

  shell$ python setup.py install

In the case where you do not have writing permissions to the system-wide
``site-packages`` directory, a local ``site-packages`` should be provided when
installing, e.g.::

  shell$ python setup.py install --prefix=$LOCAL_PYTHON_DIR

and the package will be installed in
``$LOCAL_PYTHON_DIR/lib/python-2.6/site-packages`` (assuming you are using
Python 2.6)

Documentation
=============

The documentation can be rebuilt from source using Sphinx::

  shell$ cd doc/reference
  shell$ make html

The documentation is in `build/html`.
