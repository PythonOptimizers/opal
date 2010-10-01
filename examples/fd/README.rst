Example of algorithmic tuning
=============================

This simple example demonstrates OPAL usage on the simple problem of adjusting
the finite-difference parameter for the computation of an approximation to the
first-order derivative of a noise-free function.

The example uses the function f(x) = sin(x) and approximates the derivative
using the formula

|   f(x) ≠ (f(x+h) - f(x))/h

where h > 0 is the finite-difference parameter. It is known that if f is
continuously differentiable and noise free, an optimal value of h---i.e.,
minimizing the approximation and roundoff errors---is located around the square
root of the machine epsilon. On platforms using IEEE double precision
arithmetic, this value is around 1.0e-8.

