# OPAL---A Framework for Optimization of Algorithms

## What is OPAL?

OPAL is a Python modeling language for algorithmic optimization. Most
algorithms depend on parameters. Although changing the values of those
parameters doesn't affect the correctness of the algorithm, it typically
affects its performance, where *performance* is understood broadly. How can we
best choose those parameter values so as to maximize a certain measure of
performance?

OPAL is a framework that allows to easily declare algorithms and the parameters
on which they depend along with representative test cases. It provides a
convenient syntax to formulate the optimization problem to be solved. A
black-box optimization solver takes care of the rest.

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

## References

+ [Optimization of Algorithms with OPAL](http://www.gerad.ca/~orban/_static/opalpaper.pdf)
+ [Templating and Automatic Code Generation for Performance with Python](http://www.gerad.ca/~orban/_static/templating.pdf)
+ [Taking Advantage of Parallelism in Algorithmic Parameter Optimization](http://dx.doi.org/10.1007/s11590-011-0428-6)
+ [Algorithmic Parameter Optimization of the DFO Method with the OPAL Framework](http://dx.doi.org/10.1007/978-1-4419-6935-4_15)

## Licensing

[![LGPL-3.0](http://www.gnu.org/graphics/lgplv3-88x31.png)](http://www.gnu.org/licenses/lgpl-3.0.html)
