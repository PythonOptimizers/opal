# Simple forward finite-difference approximation.
from numpy import inf

def fd(f, x, h):
    # Return the foward finite-difference approximation to df(x).
    if h == 0.0: return inf
    return (f(x+h) - f(x))/h

