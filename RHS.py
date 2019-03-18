from math import *
import numpy as np

def RHS(x, t, u):

    deg2rad = pi/180.0
    g = 9.81

    m  = 1000
    Iy = 1000
    S  = 7.0
    ro = 1.2
    cx = 0.7
    rk = 2.0
    b = 7.0

    vx = x[0]
    vy = x[1]
    om = x[2]
    teta = x[5]

    alpha = atan(vy/vx)
    V = sqrt(vy*vy + vx*vx)

    D = 0.5*ro*V*V*S*cx

    Power = 20*735.5
    Moment = Power*u[0]
    F_nap = Moment/rk

    c_om = -10.1*1
    c_vy =  1.0e+6
    Fb = 10000

    delta = u[1]

    dx_dt = np.zeros((np.size(x)))
    dx_dt[0] = (F_nap - D*cos(alpha))/m  -  om*vy
    dx_dt[1] = (Fb*delta*1 - D*sin(alpha) - c_vy*vy)/m + om*vx
    dx_dt[2] = (Fb*delta*b + c_om*om)/Iy
    dx_dt[3] = vx*cos(teta) - vy*sin(teta)
    dx_dt[4] = vx*sin(teta) + vy*cos(teta)
    dx_dt[5] = om

    return dx_dt

