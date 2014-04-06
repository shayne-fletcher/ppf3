import numpy

def solve_tridiagonal_system(N, a, b, c, r):
  """Efficiently solve a tridiagonal system.

  For example if,
  
   x +  y = 3
   y +  z = 5
   y + 2z = 8

  then, 

  A = 3x3
      [   1    1    0   
          0    1    1
          0    1    2 ]

  and r = [ 3, 5, 8 ]' for which the expected
  result is x = [1, 2, 3].

  >>> a, b, c = [None, 0, 1], [1, 1, 2], [1, 1, None]
  >>> r =[3, 5, 8]
  >>> print solve_tridiagonal_system(3, a, b, c, r)
  [ 1.  2.  3.]
  
  """
  u, gam = numpy.zeros(N), numpy.zeros(N)
  bet = b[0]
  if bet == 0.0:
    raise RuntimeError ("Solve diagonal system error")
  u[0] = r[0]/bet
  for j in range(1, N):
    gam[j] = c[j - 1]/bet
    bet = b[j]- a[j]*gam[j]
    if bet == 0.0:
      raise RuntimeError ("Solve diagonal system error")
    u[j] = (r[j] - a[j]*u[j - 1])/bet
  for j in range(N - 2, -1, -1):
    u[j] -= gam[j + 1]*u[j + 1]

  return u

def solve_upper_diagonal_system(a, b):
  """Efficiently solve an upper diagonal system.

  For example, if

    A = 3 x 3
        [  1.75   1.5   -2.5
           0     -0.5    0.65
           0      0      0.25 ]
  and

    b = [  0.5   -1      3.5],

  the expected result is x = [2.97142857  20.2  14].
  
  >>> from numpy import *
  >>> A = matrix(array(
  ... [[1.75, 1.5, -2.5],
  ... [0.0, -0.5, 0.65],
  ... [0.0, 0.0, 0.25]], float))
  >>> A
  matrix([[ 1.75,  1.5 , -2.5 ],
          [ 0.  , -0.5 ,  0.65],
          [ 0.  ,  0.  ,  0.25]])
  >>> b = array([0.5, -1.0, 3.5])
  >>> b
  array([ 0.5, -1. ,  3.5])
  >>> x = solve_upper_diagonal_system(A, b)
  >>> x = matrix(x).transpose() # column vector
  >>> x
  matrix([[  2.97142857],
          [ 20.2       ],
          [ 14.        ]])
  >>> A*x  #matrix vector product
  matrix([[ 0.5],
          [-1. ],
          [ 3.5]])

  """
  if len(a.shape) != 2:
    raise RuntimeError ("Expected 'a' to be a matrix")
  if a.shape[0] != a.shape[1]:
    raise RuntimeError ("Expected 'a' to be a square matrix")
  if len(b.shape) != 1:
    raise RuntimeError ("Expected 'b' to be a column vector")
  if b.shape[0] != a.shape[0]:
    raise RuntimeError ("Expected 'b' to be a column vector")
  N = a.shape[0]
  for i in range(N):
    if a[i, i] == 0.0:
      raise RuntimeError ("Singular upper diagonal matrix")
    for j in range(0, i):
      if a[i, j] != 0.0: raise RuntimeError ("Matrix not upper diagonal")
      
  x = numpy.zeros(N)
  for i in range(N-1, -1, -1):
    tmp = 0.0
    for j in range(i+1, N):
      tmp += a[i, j]*x[j]
    x[i] = (b[i]-tmp)/a[i, i]

  return x

def singular_value_decomposition_back_substitution(u, w, v, b):
  """Solve an upper diagonal system using svd.

  For example, if

    A = 3 x 3
        [  1.75   1.5   -2.5
           0     -0.5    0.65
           0      0      0.25 ]
  and

    b = [  0.5   -1      3.5],

  the expected result is x = [2.97142857  20.2  14].
  >>> from numpy import *
  >>> from numpy.linalg import svd
  >>> A = matrix(array(
  ... [[1.75, 1.5, -2.5],
  ... [0.0, -0.5, 0.65],
  ... [0.0, 0.0, 0.25]], float))
  >>> A
  matrix([[ 1.75,  1.5 , -2.5 ],
          [ 0.  , -0.5 ,  0.65],
          [ 0.  ,  0.  ,  0.25]])
  >>> b = array([0.5, -1.0, 3.5])
  >>> b
  array([ 0.5, -1. ,  3.5])
  >>> u, w, v = svd(A)
  >>> x = singular_value_decomposition_back_substitution(u, w, v, b)
  >>> x = matrix(x).transpose() # column vector
  >>> x
  matrix([[  2.97142857],
          [ 20.2       ],
          [ 14.        ]])
  """

  if len(u.shape) != 2:
    raise RuntimeError ("Expected 'u' to be a matrix")
  if len(w.shape) != 1:
    raise RuntimeError ("Expected 'w' to be a column vector")
  if len(v.shape) != 2:
    raise RuntimeError ("Expected 'v' to be a matrix")
  if len(b.shape) != 1:
    raise RuntimeError ("Expected 'b' to be a column vector")

  m = u.shape[0]
  n = u.shape[1]

  if w.shape[0] != n:
    raise RuntimeError ("'w' column vector has incorrect size")
  if b.shape[0] != m: 
    raise RuntimeError ("'b' column vector has incorrect size")
  if v.shape[0] != n or v.shape[1] != n:
    raise RuntimeError ("'v' matrix has incorrect size")

  tmp = numpy.zeros(n)
  for j in range(n):
    s = 0.0
    if w[j] != 0:
      for i in range(m):
        s += u[i, j]*b[i]
      s /= w[j]
    tmp[j] = s
  x = numpy.zeros(n)
  for j in range(n):
    s = 0.0
    for jj in range(n):
      s += v[jj, j]*tmp[jj]
    x[j] = s
  return x  

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()

