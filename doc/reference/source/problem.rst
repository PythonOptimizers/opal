.. Parameter Optimization Problem Definition

==================
Problem Definition
==================

In the OPAL framework, an algorithmic parameter problem has the following
components:

1. A structure, which is a sort of problem template, disconnected from any
   specifics such as the particular algorithm being tuned or the particular
   test set used to tune the parameters. An example of problem structure may
   be as simple as "minimize the total CPU time" or "maximize the throughput
   subject to network constraints."

2. Data, which fills in the blanks and brings the model to life. Data, in a
   sense, instantiates the problem structure by populating it with the
   particular algorithm being tuned, the parameters being fine-tuned, the test
   set, etc.

Instead of ``problem``, we will often use the term ``model`` and we will refer
to its components as the ``model structure`` and ``model data``.

Once the model structure and model data have been defined, we can put them
together into a single composite object representing the parameter optimization
problem. It is then referred to as as ``black box model``.

In this section, we examine the particulars of model structure, model data and
black box model.


The :class:`ModelStructure` Class
=================================

.. inheritance-diagram:: opal.core.modelstructure

.. automodule:: opal.core.modelstructure
   
.. autoclass:: ModelStructure
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:

The :class:`ModelData` Class
============================

.. inheritance-diagram:: opal.core.modeldata

.. automodule:: opal.core.modeldata
   
.. autoclass:: ModelData
   :show-inheritance: 
   :members: 
   :inherited-members: 
   :undoc-members:

The :class:`BlackBoxModel` Class
================================
