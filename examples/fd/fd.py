# Simple forward finite-difference approximation.

def fd(f, x, h):
    # Return the forward finite-difference approximation to df(x).
    if h == 0.0: return float("infinity")
    return (f(x+h) - f(x))/h

