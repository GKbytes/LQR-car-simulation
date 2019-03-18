from math import *
from path import path

def get_theta(x):
    y_ref = path(x)
    dx = 0.000001
    y_ref_dx = path(x+dx)
    teta_ref = atan((y_ref_dx - y_ref)/dx)

    return teta_ref
