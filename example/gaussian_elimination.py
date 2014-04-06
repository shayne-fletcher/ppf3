import numpy
from numpy import dot

def gaussian_elimination(a, b):
  n = len(b)
  for k in range(0, n - 1):
    for i in range(k + 1, n):
      lam = a[i, k]/a[k, k]
      a[i, k:n] -= lam*a[k, k:n]
      b[i] -= lam*b[k]
  for k in range(n - 1, -1, -1):
    b[k] = (b[k] - dot(a[k, k + 1:n], b[k + 1:n]))/a[k, k]

  return b

if __name__ == "__main__":
  a = numpy.array(
      [[ 4.,  -2.,  1.],
       [-2.,   4., -2.],
       [ 1.,  -2.,  4.]])
  b = numpy.array([[11.],[-16.],[17.]])
  x = gaussian_elimination(a.copy(), b)
  print x
  print dot(a, x)
