import numpy as np
from numpy.linalg import inv

def euler_method(RHS, x, t, dt, u):
    c_bet = 1.0
    del_state = 1.0e-6
    coef = - c_bet/del_state
    n = np.size(x)
    y = np.zeros((n,1))
    Jacob = np.zeros((n,n))
    y0 = RHS(x, t, u)

    for i in range(n):
        tmp = x[i]
        x[i] += del_state
        vec = RHS(x, t, u)
        x[i] = tmp
        Jacob[:,i] = coef * (vec - y0)

    Jacob += np.identity(n) / dt
    dx = np.matmul(inv(Jacob), y0)
    y = x + dx

    return y
