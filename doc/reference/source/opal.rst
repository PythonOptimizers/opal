.. Description of objects.

===========================
OPAL components description
===========================


Core objects
============

.. automodule:: opal.core.data

Data
----

.. autoclass:: Data
   :show-inheritance:
   :members:
   :inherited-members:
   :undoc-members:

DataSet
-------

.. autoclass:: DataSet
   :show-inheritance:
   :members:
   :inherited-members:
   :undoc-members:


Basic objects
=============

Parameter
---------

.. inheritance-diagram:: opal.core.parameter

.. automodule:: opal.core.parameter

.. autoclass:: Parameter
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:

.. autoclass:: ParameterSet
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:

.. autoclass:: ParameterConstraint
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:



Measure
-------

.. inheritance-diagram:: opal.core.measure

.. automodule:: opal.core.measure

.. autoclass:: Measure
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:

MeasureTable
------------

.. autoclass:: MeasureValueTable
    :show-inheritance: 
    :members: 
    :inherited-members: 
    :undoc-members:

Problem
-------

.. inheritance-diagram:: opal.core.testproblem

.. automodule:: opal.core.testproblem

.. autoclass:: TestProblem
    :show-inheritance: 
    :members: 
    :inherited-members: 
    :undoc-members:

.. autoclass:: OptimizationTestProblem
    :show-inheritance: 
    :members: 
    :inherited-members: 
    :undoc-members:

Algorithm experiment description object
=======================================



Parameter Optimization Problem Definition
=========================================

In the OPAL framework, a parameter optimization model (shortly OPAL model) has 
the following components:

#. A structure, which is a sort of optimization problem template, disconnected 
   from any specifics such as the particular algorithm being tuned or the particular
   test set used to tune the parameters. An example of problem structure may
   be as simple as "minimize the total CPU time" or "maximize the throughput
   subject to network constraints."

#. Data, which fills in the blanks and brings the model to life. Data, in a
   sense, instantiates the problem structure by populating it with the
   particular algorithm being tuned, the parameters being fine-tuned, the test
   set, etc.

Instead of ``problem``, we will often use the term ``model`` and we will refer
to its components as the ``model structure`` and ``model data``.

Once the model structure and model data have been defined, we can put them
together into a single composite object representing the parameter optimization
problem. It is then referred to as as ``black box model``.


Algorithm experiment
--------------------  

.. automodule:: opal.core.algorithm

.. autoclass:: Algorithm
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:

The most important ingredients of an algorithmic parameter optimization problem
are:

  #. The algorithm to be fine tuned,
  #. The parameters to fine tune,
  #. The measures defining the performance criterion.


In this section, we examine the basic ingredients in detail.


In this section, we examine the particulars of model structure, model data and
black box model.


ModelStructure
---------------------------------

.. automodule:: opal.core.modelstructure

.. autoclass:: ModelStructure
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:

ModelData
----------------------------

.. automodule:: opal.core.modeldata

.. autoclass:: ModelData
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:

Model
--------------------------------

.. automodule:: opal.core.blackbox

.. autoclass:: BlackBoxModel
   :show-inheritance:
   :members:
   :inherited-members:
   :undoc-members:



