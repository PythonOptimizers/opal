.. Tutorial on interfacing a new algorithm.

=====================================
Tutorial: Interfacing a New Algorithm
=====================================

Interfacing a new algorithm with the goal of improving its performance in some
sense is done in three steps. This tutorial walks the reader through those
steps and provides examples.


Step 1: Specifying the Algorithm Description
============================================

In this step, we ``declare`` the new algorithm by subclassing the `Algorithm`
abstract class. This is easy: we give the algorithm a name, specify its
purpose and emphasize its most important components from the point of view of
OPAL: its parameters. While specifying parameters, we specify their ``kind``
and ``domain``.

.. todo::

    Expand description.

Step 2: Modeling the Parameter Optimization Problem
===================================================

Once the algorithm is in place, and we got that out of the way, we can get to
the meat: the parameter optimization problem. In this step, we use the
parameters of our new algorithm to formulate the problem based on existing or
newly-defined ``performance measures``. In particular, we use such measures to
define the objective and constraints (if any) of our problem.

.. todo::

    Expand description.

Step 3: Writing the Black Box
=============================

In this last step, we describe the black box that is at the interface between
OPAL and our algorithm. OPAL calls the black box which in turn calls the
algorithm with parameter values specified by OPAL. Upon return from the
algorithm, it is the role of the black box to return all relevant performance
measures---those same measures that appear in Step 2.

.. todo::

    Expand description.
