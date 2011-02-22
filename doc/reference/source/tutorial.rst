.. Tutorial on interfacing a new algorithm.

================================================
Tutorial: Simple tasks of Parameter Optimization
================================================

Invoke a simple session of algorithmic parameter optimization in some
sense is done in three steps:

#. Create a wrapper that are actually an executable. This executable describes
   how to test the algorithm.

#. Declare all neccessary components of an algorithmic parameter optimization.
   This step is realized by the OPAL-syntax statements that can be found in a
   declaration file or main file.

#. Create main file that contains the statments to provoke a session of optimization
   and may be some declarations of formulating a parameter optimization problem.

Pratically, we need create at three files: an executable wrapper, a decralation and
a main file. The contents of wrapper is easily seperated from the others, and
can be written in any programming language. The content of declaration file and main file
are written in Python and follow the OPAL syntax.

This tutorial walks the reader through those steps by some simple examples.

Getting started by optimizing the `finite-difference` algorithm
===============================================================

The first example shows how to identify the optimal small value of *finite difference* formula.

`Finite-difference` method to approximate derivative according to the formula. It  has one parameter that is
a small value `h`

.. math::
   \delta_f(x;h) := \frac{f(x + h) - f(x)}{h} \approx f'(x)

An implementation in a form of a Python module is illustrated in
following listing::


  '''

  File fd.py
  '''
  def finite_diff(f, x, h):
      if h == 0:
 return float("infinity")
      return (f(x + h) - f(x))/h


We will explain step by step the example. Each step results in a Python file
that called generally *wrapper file*, *declaration file* and *main file*

**Create wrapper file**

A wrapper is actually a description of communication between the target algorithm
and OPAL. This shoulds show at least the follwoing information:

#. How the parameter values are transfered from OPAL to the target algorithm and how
   they are set as ready to execute algorithm.

#. How the algorithm is invoked to solve a problem.

#. How the elemetary measure values are collected from the executtion result and
   transfered to OPAL.

There are two options to create a wrapper. The first case demands an :ref:`executable
wrapper<creating_of_wrapper>` and some :ref:`statements to declare this to OPAL<declaration_to_opal>`.
The second option  is sub-classing the `Algorithm` class. The later is more
complicated and reserved to Python-exeperient users. We choose the former to show this example.

.. _creating_of_wrapper:

*Creating of wrapper*

An executable wrapper can be generally written in any programming language but has following
restrictions:

#. OPAL considered a wrapper as a shell-executable program with three-argument. The execution
   command is ::

     shell$ executable_command parameter_file problem_name output_file

#. The ``problem_name`` is the name of problem file

#. The format of ``parameter_file`` and ``output_file`` are predefined in OPAL and the
   users have to obey that when creating the wrapper.

#. The ``parameter_file`` contains parameter values while ``output_file`` contains elementary
   measure values

Obviously, how to create a wrapper depends on the algorithm and user experience. The follwing
listing is an example of the wrapper for the above ``finite-difference`` algorithm. This wrapper
returns the approximation error as unique observed elementary measure::


  '''

  File diff_run.py
  '''
  import sys
  import pickle

  def read_param(parameter_file, loc='.'):
    parms = {}
    f = open(parameter_file, 'rb')
    try:
        parms = pickle.load(f)
    except:
        raise IOError, 'Parameter file does not have expected format'
    f.close()
    h = parms['h'].value
    return h


  def run(problem_name, h):
    import fd
    import math
    #print h
    appVal = fd.finite_diff(math.sin, 0.0, h)
    err = abs(1.0 - appVal)
    return {'ERR' : err}

  if __name__ == '__main__':
    param_file = sys.argv[1]
    problem = sys.argv[2]
    output_file = sys.argv[3]

    h = read_param(param_file)
    measure_values = run(problem, h)

    f = open(output_file,'w')
    for measure in measure_values.keys():
        print >> f, measure, measure_values[measure]
    f.close()


Some points should be noted in the above listing:

#. The wrapper communicates avec the OPAL through the immediated files. By default, the format of these files are pre-defined in
   two methods :func:`Algorithm.write_parameter` and :func:`Algorithm.read_measure`. The paramters are loaded
   in a directory by module :mod:`pickle`, the same module is used to write parameters.  Meanwhile, the measures are written
   line by line, each line corresponds to a measure.

#. The argument processing follows exactly the order of arguments in a wrapper call.

#. The algorithm is involved by ``import fd`` statement and the function call ``fd.finite_diff(math.sin, 0.0, h)``.


.. _declaration_to_opal

**Declare to OPAL**

The declarations can be spread into two files and include wrapper declaration, parameter optimization problem
declaration and solver declaration.

Meanwhile the wrapper can be implemented in
any programing language, the declarations should be written in Python and follow the
principles of OPAL:

#. The wrapper is represented by an :class:`Algorithm` object with at least a name and the name
   to execute the wrapper

#. The parameters are defined as :class:`Parameter` objects

#. The measures are defined as :class:`Measure` objects

#. The feasible region of parameters are defined by the :class:`ParameterConstraint`. The condition is
   provided by a string, for example `h > 0`

An example of declaration file is show in following listing ::


  from opal.core.parameter import Parameter
  from opal.core.measure import Measure
  from opal.core.algorithm import Algorithm

  # Define new algorithm
  FD = Algorithm(name='FD', purpose='Finite Difference')

  # Register executable for FD
  FD.set_executable_command('python diff_run.py')

  # Register immediated parameter file for communicating with wrapper
  FD.set_parameter_file('diff.param')

  # Define parameters
  h = Parameter(kind='real', default=0.5, name='h', bound=[0, None])

  # Register parameters with algorithm
  FD.add_param(h)

  FD.add_parameter_constraint('h >= 0')

  # Define and register the measures
  FD.add_measure(Measure(kind="real", name='ERR', description='Error of the approximation'))


**Create an optimization session**

We create a session in a Python file called `main file`. We call this the main file because
the command to provoke the optimization process
should be placed in this file. However, beside this command, some other declarative
statements are ussually found in this file. In this example, we leave all the statements
that declare a problem of parameter optimization in this file to highlight the most
important step: **interfacing an algorithm to OPAL**.

Once the algorithm is in place, and we got that out of the way, we can get to
the meat: the parameter optimization problem. In this step, we use the
parameters of our new algorithm to formulate the problem based on existing or
newly-defined ``performance measures``. In particular, we use such measures to
define the objective and constraints (if any) of our problem.

A main file that desires to minimize the small value ``h`` is defined as following listing::


  '''
  The diff_tune.py
  '''

  from diff_decl import FD

  from opal import ModelStructure
  from opal import ModelData
  from opal import BlackBoxModel

  from opal.Solvers import NOMAD

  def sum_err(parameters,measures):
    return sum(measures["ERR"])

  # Select all parameters.
  params = [par for par in FD.parameters]

  # The problem set is empty
  problems = []

  data = ModelData(FD, problems, params)
  structure = ModelStructure(objective=sum_err, constraints=[])  # Unconstrained

  # Instantiate black-box solver.
  blackbox = BlackBoxModel(modelData=data,modelStructure=structure)
  NOMAD.solve(model=blackbox)


In this listing, all statements from the begin except the last one are declarations.
They show that, all of algorithm's parameter are involved to the minimization of
approximation error. The last one figures out that, NOMAD is chosen as the solver and
it is invoked by method :func:`solve`.

Now, to run this example, from the prompt of shell environment, we launch::

  shell$ python diff_tune.py

The output on screen looklikes ::

  NOMAD - version 3.4.1 - www.gerad.ca/nomad

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

	EVAL	BBE	[	SOL,	]	OBJ	TIME	\\

	1	1	[	0.5 	]	0.04114892279	0	\\
	4	4	[	0.25 	]	0.01038416298	0	\\
	12	8	[	0.1875 	]	0.005849083935	1	\\
	16	11	[	0.125 	]	0.002602132918	1	\\
	20	14	[	0.0625 	]	0.0006509145219	2	\\
	28	17	[	0.0380859375 	]	0.000241738906	2	\\
	32	21	[	0.013671875 	]	3.115306984e-05	3	\\
	40	28	[	0.006286621094 	]	6.586921113e-06	4	\\
	46	33	[	0.002380371094 	]	9.443608232e-07	5	\\
	52	37	[	0.0005340576172 	]	4.753625571e-08\\
	60	43	[	5.125999451e-05 	]	4.379312468e-10\\
	72	54	[	2.074893564e-05 	]	7.175304795e-11\\
	78	59	[	5.490146577e-06 	]	5.023537142e-12\\
	86	65	[	1.675449312e-06 	]	4.678479826e-1310	\\
	94	71	[	7.217749953e-07 	]	8.681944053e-1411	\\
	100	75	[	2.450397005e-07 	]	9.992007222e-1512	\\
	106	79	[	6.621121429e-09 	]	0	12	\\
	153	124	[	6.621121429e-09 	]	0	21	\\

  } end of run (mesh size reached NOMAD precision)

  black-box evaluations   : 124
  best feasible solution  : ( 6.621121429e-09 ) h=0 f=0


This also shows that first example is successful. That verifies the theory result indicating that
:math:`h^* = O(\sqrt{\epsilon_{machine}}) \approx 10^{-8}`

..
  Example of surrogate
  ====================

Describe an algorithm by sub-classing `Algorithm`
=================================================

In this step, we *declare* the new algorithm by subclassing the `Algorithm`
abstract class. This is easy: we give the algorithm a name, specify its
purpose and emphasize its most important components from the point of view of
OPAL: its parameters. While specifying parameters, we specify their ``type``,
default value and ``domain``. The list of observed elementary measures is optionally
declared because we may be don't need any information from the running result.
The following code illustrates how to declare an algorithm::

   from opal.parameter import Parameter
   from opal.measure import Measure
   from opal.algorithm import Algorithm

   class DifferenceFinite(Algorithm):
     def __init__(self):
       Algorithm.__init__(self,
                          name='Diff-finite',
                          purpose='Approximate the derivative basing on difference finite',
			  parameter=[Parameter(name='h',
                                               dtype='real',
					       default=0.5)],
                          input=None,
                          output=[Measure(name='ERROR',
                                          dtype='real',
                                          dimension=1)])
       self.argument_string = ''
       return



After declaring the algorithm, we have to create an interface to the OPAL for this
new algorithm. OPAL needs to know three things to work with a target algorithm:

  #. How to set parameters of the target algorithm
  #. How to run the target algorithm
  #. How to get elementary measures from the running


Specifying these things is essentially overwrite two virtual methods of `Algorithm`
abstract class: `set_parameter()`, `run()`. The `set_parameter()` accepts the arguments
as values of the parameters and let them effective, for example, write them all to
parameter file. The method :func:`set_parameter()` of :class: Algorithm by default, is
not empty, it set parameter values to parameter set. Hence, the customized method
`set_parameter()` is recommend call :func:`Algorithm.set_parameter` before do anything
else.

For this example, to make the parameter effective, the value of the parameter is set to
the argument string::

  class DifferenceFinite(Algorithm):
    def __init__(self):
      '''
      Definition of constructor
      '''
      return

    def set_parameter(self,parameterValues=None):
      '''
      Set the values to the parameter set.
      Just call the default set_parameter() of the Algorithm abstract class
      '''
      Algorithm.set_parameter(self,parameterValues=parameterValues)
      '''
      Make the parameters effective
      '''
      if parameterValues is None:
        self.argument_string = str(self.parameter['h'].default)
      else:
        self.argument_string = str(self.parameter['h'].value)
      return


The algorithm is activated by command line with two arguments representing for the value
of parameter and the point where we want to evaluate derivative, for example::

   shell$ python diff 0.5 -1.25

The output sent to output standard includes two values: the derivative value and its error.
We capture just second value among two outputed values. The code of :func:`run()` is shown
in following::

  class DifferenceFinite(Algorithm):
    def __init__(self):
      '''
      Definition of the constructor
      '''
      return

    def set_parameter(self,parameterValues=None):
      '''
      Definition of set_parameter() method
      '''
      return

    def run(self,inputValues=None):
      import subprocess

      proc = subprocess.Popen("python diff.py " + self.argument_string + " 0.0" ,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

      stdOutputs = proc.communicate() #  The process output content is registered
      '''
      We consider the second word of string get from the standard output (the
      first element in the list stdOutputs) is
      the desired value
      '''
      words = stdOutputs[0].split(' ')

      self.output.set_values(values=[words[1]])
      return self.output


.. todo::

    Expand description.




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



.. todo::

    Expand description.


