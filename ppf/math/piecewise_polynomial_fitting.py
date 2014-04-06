import math
import numpy
from .linear_algebra import *

def piecewise_cubic_fit(x, y):
  """Fit data piecewise to a cubic polynomial

  For example fit 1.5+0.5x+0.25x^2-2.25x^3:

  >>> from numpy import *
  >>> x = linspace(-1.5, 1.5, 7)
  >>> y = zeros(7)
  >>> for i in range(0, 7):
  ...   y[i] = 1.5+0.5*x[i]+0.25*x[i]*x[i]-2.25*x[i]*x[i]*x[i]
  >>> c = piecewise_cubic_fit(x, y)
  >>> c
  array([[ 1.5 ,  1.5 ,  1.5 ],
         [ 0.5 ,  0.5 ,  0.5 ],
         [ 0.25,  0.25,  0.25],
         [-2.25, -2.25, -2.25]])

  """

  if len(x.shape) != len(y.shape) and len(x.shape) != 1:
    raise RuntimeError ("Mismatching 'x' and 'y' vectors")
  if x.shape[0] != y.shape[0]:
    raise RuntimeError ("Mismatching 'x' and 'y' vectors")
  N = x.shape[0]
  if N < 4:
    raise RuntimeError ("Need at least 4 points")

  # assume uniform spacing
  one_sixth = 1.0/6.0
  four_thirds = 4.0/3.0
  dx_inv = 1.0/(x[1]-x[0])
  dx_inv2 = dx_inv*dx_inv
  dx_inv3 = dx_inv2*dx_inv
  coeffs = numpy.zeros((4, N - 4))

  a = numpy.zeros((4, 4))
  b = numpy.zeros(4)

  for i in range(2, N-2):
    # value
    b[0] = y[i]
    # first derivative
    b[1] = (one_sixth*(-y[i+2]+y[i-2])+four_thirds*(y[i+1]-y[i-1]))*0.5*dx_inv
    # second derivative
    b[2] = (y[i+1]-2.0*y[i]+y[i-1])*dx_inv2
    # third derivative
    b[3] = (y[i+2]-2.0*(y[i+1]-y[i-1])-y[i-2])*0.5*dx_inv3

    # fit matrix
    xi = x[i]
    xi2 = xi*xi
    xi3 = xi2*xi
    a[0][0] = 1.0
    a[0][1] = xi
    a[0][2] = xi2
    a[0][3] = xi3
    a[1][1] = 1.0
    a[1][2] = 2.0*xi
    a[1][3] = 3.0*xi2
    a[2][2] = 2.0
    a[2][3] = 6.0*xi
    a[3][3] = 6.0

    tmp = solve_upper_diagonal_system(a, b)
    for j in range(0, 4):
      coeffs[j, i-2] = tmp[j] 

  return coeffs

def  _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
