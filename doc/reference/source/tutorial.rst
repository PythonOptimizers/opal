.. Tutorial on interfacing a new algorithm.

================================================
Tutorial: Simple tasks of Parameter Optimization
================================================

A simple session of algorithmic parameter optimization
consists in three steps:

#. Declare the target algorithm to OPAL along with its parameters and the
   measures that it outputs. We refer to such measures as ``atomic``.

#. Define an algorithmic parameter optimization problem based on some or all of
   the parameters and using the atomic measures to construct an objective
   function and (possibly) some constraints.

#. Pass the resulting problem to the black-box solver.

Pratically, we need create an executable wrapper, and one or more Python files for
declaring, defining parameter optimization problem and activating solving session.
The contents of wrapper is easily seperated from the others, and
can be written in any programming language and satisfies some simple restrictions
relating input and output. The target algorithm declartion, parameter optimization
problem definition, session provoking are written in Python and follow the OPAL
syntax. We can spread the Python code in one or more Python files.

This tutorial walks the reader through those steps by some simple examples.

Getting started by optimizing the `finite-difference` algorithm
===============================================================

The first example shows how to identify an optimal step size in a *forward
finite difference* formula. In forward finite differences, the derivative at
:math:`x` of a function :math:`f` of a single variable is approximated using
the formula

.. math::

   \delta f(x;h) := \frac{f(x + h) - f(x)}{h} \approx f'(x)

In this formula, we could consider the step size :math:`h` as a real parameter.

Here is a possible (simple) Python implementation

.. literalinclude:: /examples/fd/fd.py 

We will explain step by step the example. In this example, the executable
wrapper is written in Python. The declaration, definition of OPAL problem are
separated from the provoking session. Hence, each step results in a Python file
that called generally *wrapper file*, *declaration file* and *main file*. We
push the declaration part into a separated file to reuse it as we want to
optimize the algorithm in different maners.

.. _creating_of_wrapper:

Creating of wrapper
-------------------

A wrapper is actually a description of communication between the target algorithm
and OPAL. This shoulds show at least the follwoing information:

#. How the parameter values are transfered from OPAL to the target algorithm and how
   they are set as ready to execute algorithm.

#. How the algorithm is invoked to solve a problem whose name is provided by OPAL.

#. How the elemetary measure values are collected from the executtion result and
   transfered to OPAL.

There are two options to create a wrapper. The first case demands an :ref:`executable
wrapper<creating_of_wrapper>` and some :ref:`statements to declare this to OPAL<declaration_to_opal>`.
The second option  is sub-classing the `Algorithm` class. The later is more
complicated and reserved to Python-exeperient users. We choose the former to show this example.

An executable wrapper can be generally written in any programming language but has following
restrictions:

#. OPAL considered a wrapper as a shell-executable program with three-argument. The execution
   command is ::

     shell$ executable_command parameter_file problem_name output_file

#. The ``problem_name`` is the name of problem file

#. The ``parameter_file`` contains parameter values while ``output_file`` contains elementary
   measure values. The format of ``parameter_file`` and ``output_file`` are predefined in OPAL and the
   users have to obey that when creating the wrapper.

Obviously, how to create a wrapper depends on the algorithm and user experience. The follwing
listing is an example of the wrapper for the above ``finite-difference`` algorithm. This wrapper
returns the approximation error as unique observed elementary measure

.. literalinclude:: /examples/fd/fd_run.py 

Some points should be noted in the above listing:

#. The wrapper communicates avec the OPAL through the immediated files whose format is fixed by OPAL. 
   As the executable wrapper are written in Python, we can benefit two predefined methods 
   :func:`opal.core.io.read_parameter` and
   :func:`opal.core.io.write_measure` to take care the reading parameters from file and writing measures to file.
   This is one of the advantage as creating executable wrapper by Python.

#. The argument processing follows exactly the order of arguments in a wrapper call.

#. The algorithm is involved by ``import fd`` statement and the function call ``fd(math.sin, 0.0, h)``.
   Module ``fd`` provides the ``fd`` routine to compute difference of given function specified by the first 
   argument.
   The wrapper will test this routine with function :math:`sin(x)` at point :math:`x=\pi/4`.


.. _declaration_to_opal:

Declare to OPAL
---------------

Meanwhile the wrapper can be implemented in
any programing language, the declarations should be written in Python and follow the
principles of OPAL:

#. The wrapper is represented by an :class:`Algorithm` object with at least a name and the name
   to execute the wrapper

#. The parameters are defined as :class:`Parameter` objects

#. The measures are defined as :class:`Measure` objects

#. The feasible region of parameters are defined by the :class:`ParameterConstraint`. The condition is
   provided by a string, for example `h > 0`

An example of declaration file is show in following listing 

.. literalinclude:: /examples/fd/fd_declaration.py 


Create an optimization session
------------------------------

We create a session in a Python file called `main file`. We call this the main file because
the command to provoke the optimization process
should be placed in this file. However, beside this command, some other declarative
statements are usually found in this file. In this example, we leave all the statements
that declare a problem of parameter optimization in this file to highlight the most
important step: **interfacing an algorithm to OPAL**.

Once the algorithm is in place, and we got that out of the way, we can get to
the meat: the parameter optimization problem. In this step, we use the
parameters of our new algorithm to formulate the problem based on existing or
newly-defined ``performance measures``. In particular, we use such measures to
define the objective and constraints (if any) of our problem.

A main file that desires to minimize the small value ``h`` is defined as following listing

.. literalinclude:: /examples/fd/fd_optimize.py 

In this listing, all statements from the begin except the last one are declarations.
They show that, all of algorithm's parameter are involved to the minimization of
approximation error. The last one figures out that, NOMAD is chosen as the solver and
it is invoked by method :func:`solve`.

Now, to run this example, from the prompt of shell environment, we launch::

  shell$ python fd_optimize.py

The output on screen looks like ::


  NOMAD - version 3.4.2 - www.gerad.ca/nomad

  Copyright (C) 2001-2010 {
        Mark A. Abramson     - The Boeing Company
    Charles Audet        - Ecole Polytechnique de Montreal
    Gilles Couture       - Ecole Polytechnique de Montreal
    John E. Dennis, Jr.  - Rice University
    Sebastien Le Digabel - Ecole Polytechnique de Montreal
  }

  Funded in part by AFOSR and Exxon Mobil.

  License   : '$NOMAD_HOME/src/lgpl.txt'
  User guide: '$NOMAD_HOME/doc/user_guide.pdf'
  Examples  : '$NOMAD_HOME/examples'
  Tools     : '$NOMAD_HOME/tools'

  Please report bugs to nomad@gerad.ca

  MADS run {

    EVAL    BBE [   SOL,    ]   OBJ TIME    \\

    1   1   [   0.5     ]   0.2022210836       1    \\
    4   4   [   0.25    ]   0.09527166174      2    \\
    12  8   [   0.1875  ]   0.07023320242      4    \\
    16  11  [   0.125   ]   0.04597664512      5    \\
    20  14  [   0.0625  ]   0.02255016086      7    \\
    28  17  [   0.0380859375    ]   0.01363471996      9    \\
    32  21  [   0.013671875     ]   0.004855691016    10    \\
    40  28  [   0.006286621094  ]   0.002227306539    13    \\
    46  33  [   0.002380371094  ]   0.0008422556376   15    \\
    52  37  [   0.0005340576172     ]   0.0001888514898   16    \\
    60  43  [   5.125999451e-05     ]   1.812345385e-05   19    \\
    72  54  [   2.074893564e-05     ]   7.335906448e-06   24    \\
    78  59  [   5.490146577e-06     ]   1.941051869e-06   26    \\
    86  65  [   1.675449312e-06     ]   5.923241065e-07   28    \\
    94  71  [   7.217749953e-07     ]   2.551989452e-07   31    \\
    100 75  [   2.450397005e-07     ]   8.67597334e-08    33    \\
    106 79  [   6.621121429e-09     ]   3.704942908e-09   34    \\
    121 92  [   1.407139655e-08     ]   3.174716379e-09   40    \\
    128 98  [   1.779668685e-08     ]   6.411027265e-10   42    \\
    162 130 [   1.779657316e-08     ]   1.926234727e-10   61    \\
    167 132 [   1.779657316e-08     ]   1.926234727e-10   62    \\

  } end of run (mesh size reached NOMAD precision)

  blackbox evaluations    : 132
  best feasible solution  : ( 1.779657316e-08 ) h=0 f=1.926234727e-10
  Expected optimal value is approximately 1.490116119384766e-08


The black-box solver identified 1.779657316e-08 as the optimal step size. This
first example is thus successful because the theory indicates that :math:`h^* =
O(\sqrt{\epsilon_{machine}}) \approx 10^{-8}`

..
  Example of surrogate
  ====================

..
  .. todo::
  Expand description.



..
  .. todo::
  Expand description.

..
  Step 3: Writing the Black Box
  =============================

  In this last step, we describe the black box that is at the interface between
  OPAL and our algorithm. OPAL calls the black box which in turn calls the
  algorithm with parameter values specified by OPAL. Upon return from the
  algorithm, it is the role of the black box to return all relevant performance
  measures---those same measures that appear in Step 2.



..
  .. todo::
  Expand description.


