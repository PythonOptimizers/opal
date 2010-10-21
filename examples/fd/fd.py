# Simple forward finite-difference approximation.

def fd(f, x, h):
    # Return the foward finite-difference approximation to df(x).
    if h == 0.0: return float("infinity")
    return (f(x+h) - f(x))/h

