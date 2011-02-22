.. Introduction to OPAL

====================
Introduction to OPAL
====================

OPAL stands for **Optimization of Algorithm**. OPAL provides a framework in
which algorithmic parameter optimization problems can be defined and solved
in a programmatic way.

Our approach is formulate a parameter optimizaiton problem as a *blackbox
optimization problem*. This is so different from the popular approaches that
uses heuristic to minimize the running time as unique goal. The formulated
blackbox has the objective function and constraints built from parameter values
and elementary measures obtained from empirical tests. Hence, the users can
optimize his algorithm in any aspect and exploit any algorithmic parameter.
The blackbox problem is, in general, solved by any direct-search solver.

A parameter optimization task with OPAL need to two stubs:
 #. The target algorithm description
 #. Problem definition

OPAL is written in Python and use Python as problem definition and algorithm
description language. In general, each stub is described seperatedly into
a file and can be reused as many times as users wants. Particularly, the
target algorithm stub can be re-used when we want optimize the same algorithm
but in different maners.


.. todo::

   Add much more to this.

