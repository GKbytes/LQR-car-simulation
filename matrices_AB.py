import numpy as np

def declare_matrix(n, m):

  return np.array([[0.0 for j in range(0,m)] for i in range(0,n)])

def Jacob_AB(RHS, y, t, u_control, n, m):

  A = declare_matrix(n, n)
  B = declare_matrix(n, m)
  dy = 1.0e-6
  f0 = RHS(y, t, u_control)

  for i in range(0, n):
    yp = np.array(y)
    yp[i] += dy
    f = RHS(yp, t, u_control)

    for j in range(0, n):
      A[j, i] = (f[j] - f0[j]) / dy

  for i in range(0, m):
    up = np.array(u_control)
    up[i] += dy
    f = RHS(y, t, up)
    for j in range(0, n):
      B[j, i] = (f[j] - f0[j]) / dy

  return A, B
