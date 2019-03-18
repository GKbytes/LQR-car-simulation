from math import *

def draw_car(X, Y, teta):

    xs = [0.0 for i in range(5)]
    ys = [0.0 for i in range(5)]
    
    c = 2.0

    xs0 = [-0.4*c, 0.4*c, 0.4*c, -0.4*c, -0.4*c]
    ys0 = [-0.2*c, -0.2*c, 0.2*c, 0.2*c, -0.2*c]

    for i in range(5):
        xs[i] = X + xs0[i]*cos(teta) - ys0[i]*sin(teta)
        ys[i] = Y + xs0[i]*sin(teta) + ys0[i]*cos(teta)

    return xs, ys
