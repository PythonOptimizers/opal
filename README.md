# OPAL---A Framework for Optimization of Algorithms

## Requirements

+ Python version 2.6 or 2.7 (not tested with 3.x)
+ [NOMAD](http://www.gerad.ca/NOMAD)

## Install

+ Unzip the package or clone the git repository
+ Go to the source directory
+ Run `python setup.py install`

## Testing

To run the following test, [Numpy](http://www.numpy.org) is required. Install
it with `pip install numpy`.

Assuming your `PYTHONPATH` is set correctly, you should be able to do:

    cd examples/fd
    python fd_optimize.py
