# Simple forward finite-difference approximation.

from math import sin, cos
from numpy import inf

def f(x):
    # Return function value.
    return sin(x)

def df(x):
    # Return (exact) derivative of f at x.
    return cos(x)

def fd(x, h):
    # Return the foward finite-difference approximation to df(x).
    if h == 0.0: return inf
    return (f(x+h) - f(x))/h

def compute_error(x, h):
    # This is the "main program".
    return abs(df(x) - fd(x,h))

