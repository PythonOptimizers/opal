.. Description of basic objects.

=================================
Basic Components of OPAL Problems
=================================

The most important ingredients of an algorithmic parameter optimization problem
are:

1. The algorithm to be fine tuned,
2. The parameters to fine tune,
3. The measures defining the performance criterion.

In this section, we examine the basic ingredients in detail.


Algorithms: The :mod:`algorithm` Module
=======================================

.. inheritance-diagram:: opal.core.algorithm

.. automodule:: opal.core.algorithm

.. autoclass:: Algorithm
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:

Parameters: The :mod:`parameter` Module
=======================================

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


Performance Measures: The :mod:`measure` Module
===============================================

.. inheritance-diagram:: opal.core.measure

.. automodule:: opal.core.measure

.. autoclass:: Measure
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:

.. autoclass:: MeasureList
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:

.. autoclass:: MeasureTable
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:

