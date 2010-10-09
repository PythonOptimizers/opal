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

    MADS run{
    
     EVAL BBE [ SOL, ] OBJ TIME \\
    
     1 1 [ 0.5  ] 0.2022210836    0 \\
     2 2 [ 0.4  ] 0.1582516709    0 \\
     3 3 [ 0.1  ] 0.03650380828    1 \\
     11 6 [ 0.075  ] 0.0271668032    2 \\
     15 8 [ 0.05  ] 0.01796857799    3 \\
     19 10 [ 0.025  ] 0.008912029073    3 \\
     27 12 [ 0.01875  ] 0.006670363173    4 \\
     31 14 [ 0.0125  ] 0.004437773933    5 \\
     35 16 [ 0.00625  ] 0.002214305049    6 \\
     43 18 [ 0.00380859375  ] 0.001348249081    7 \\
     47 20 [ 0.0013671875  ] 0.0004835939884    8 \\
     55 23 [ 0.0006286621094  ] 0.0002223121897    9 \\
     61 25 [ 0.0002380371094  ] 8.416550444e-05    9 \\
     67 27 [ 5.340576172e-05  ] 1.88821243e-05   10 \\
     75 30 [ 5.125999451e-06  ] 1.812326825e-06   11 \\
     87 35 [ 2.074893564e-06  ] 7.335931301e-07   13 \\
     93 37 [ 5.490146577e-07  ] 1.940868919e-07   14 \\
     101 40 [ 1.675449312e-07  ] 5.898094313e-08   15 \\
     109 43 [ 7.217749951e-08  ] 2.629330675e-08   16 \\
     115 45 [ 2.450397003e-08  ] 9.569121828e-09   17 \\
     123 49 [ 1.258558766e-08  ] 2.656297737e-09   19 \\
     134 57 [ 1.407570378e-08  ] 8.138155705e-10   22 \\
     157 78 [ 1.407861414e-08  ] 3.433888729e-10   30 \\
     170 87 [ 1.407861414e-08  ] 3.433888729e-10   33 \\
    
    }end of run (mesh size reached NOMAD precision)

The outcome of the run is that the final value of the stepsize found is
h=1.407861414e-08 and the error value is 3.433888729e-10. The error is computed
as the absolute value of the difference between the "exact" derivative and
the approximation computed by finite differences.
