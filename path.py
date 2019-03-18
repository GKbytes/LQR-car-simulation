from math import *

def path(x):
    y0 = 10.0
    c = 4.0
    y_ref = y0 + c * (2.0*sin(0.02*x) + 1.0*sin(0.05*x) +
                      2.0*sin(0.07*x) + 1.0*sin(0.3*x))

    return y_ref
