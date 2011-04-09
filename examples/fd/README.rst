Example of algorithmic tuning
=============================

This simple example demonstrates OPAL usage on the simple problem of adjusting
the finite-difference parameter for the computation of an approximation to the
first-order derivative of a noise-free function.

The example uses the function f(x) = sin(x) and approximates the derivative
using the formula::

   f(x) ≠ (f(x+h) - f(x))/h

where h > 0 is the finite-difference parameter. It is known that if f is
continuously differentiable and noise free, an optimal value of h---i.e.,
minimizing the approximation and roundoff errors---is located around the square
root of the machine epsilon. On platforms using IEEE double precision
arithmetic, this value is around 1.0e-8.

Below is the output of a run on a i386 Intel Core2 Duo running OSX 10.5.8::

    NOMAD - version 3.5.0 - www.gerad.ca/nomad
    
    Copyright (C) 2001-2011 {
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
    
        BBE SOL OBJ TIME
    
          1 5.0e-01 2.022e-01    0.00
          5 2.5e-01 9.527e-02    1.00
         12 1.9e-01 7.023e-02    3.00
         15 1.2e-01 4.598e-02    4.00
         17 6.2e-02 2.255e-02    4.00
         20 3.8e-02 1.363e-02    5.00
         26 1.4e-02 4.856e-03    7.00
         37 6.3e-03 2.227e-03    9.00
         45 2.4e-03 8.423e-04   11.00
         52 5.3e-04 1.889e-04   13.00
         62 5.1e-05 1.812e-05   16.00
         79 2.1e-05 7.336e-06   21.00
         87 5.5e-06 1.941e-06   23.00
         97 1.7e-06 5.923e-07   25.00
        107 7.2e-07 2.552e-07   28.00
        114 2.5e-07 8.676e-08   30.00
        121 6.6e-09 3.705e-09   31.00
        139 1.4e-08 2.054e-09   36.00
        149 1.8e-08 1.527e-09   39.00
        150 1.2e-08 3.251e-13   40.00
        198 1.2e-08 3.251e-13   54.00
    
    } end of run (mesh size reached NOMAD precision)
    
    blackbox evaluations    : 198
    best feasible solution  : ( 1.220878909e-08 ) h=0 f=3.250733016e-13
    Expected optimal value is approximately 1.490116119384766e-08

The outcome of the run is that the final value of the stepsize found is
h=1.407861414e-08 and the error value is 3.433888729e-10. The error is computed
as the absolute value of the difference between the "exact" derivative and
the approximation computed by finite differences.
