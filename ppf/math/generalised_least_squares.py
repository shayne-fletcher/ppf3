import numpy
import random
from .linear_algebra import *

def generalised_least_squares_fit(y, x, sig, fit_fos):
  """
  >>> import math
  >>> class linear_fo(object):
  ...   def __call__(self, x):
  ...     return x[0]
  >>> class quadratic_fo(object):
  ...   def __call__(self, x):
  ...     return x[0]*x[0]
  >>> generator = random.Random(1234)
  >>> ndata = 100
  >>> sig = numpy.zeros(ndata)
  >>> sig.fill(1.0)
  >>> y = numpy.zeros(ndata)
  >>> x = numpy.zeros([ndata, 1])
  >>> a = 0.25
  >>> b = -0.1
  >>> for i in range(ndata):
  ...   v = generator.gauss(0, 1.0)
  ...   x[i, 0] = v
  ...   y[i] = a*v+b*v*v
  >>> fit_fos = []
  >>> fit_fos.append(linear_fo())
  >>> fit_fos.append(quadratic_fo())
  >>> coeffs = generalised_least_squares_fit(y, x, sig, fit_fos)
  >>> coeffs
  array([ 0.25, -0.1 ])
  """
  tol = 1.0e-13

  if len(y.shape) != 1:
    raise RuntimeError ("Expected 'y' to be a column vector")
  if len(x.shape) != 2:
    raise RuntimeError ("Expected 'x' to be a matrix")
  if len(sig.shape) != 1:
    raise RuntimeError ("Expected 'sig' to be a column vector")

  ndata = x.shape[0]
  ma = len(fit_fos)

  if sig.shape[0] != ndata:
    raise RuntimeError ("'sig' column vector has incorrect size")
  if y.shape[0] != ndata:
    raise RuntimeError ("'y' column vector has incorrect size")


  a = numpy.zeros(ma)

  if ndata == 0:
   return a
  else:
   b = numpy.zeros(ndata)
   cu = numpy.zeros([ndata, ma])

   for i in range(ndata):
     xi = x[i, :]
     tmp = 1.0/sig[i]
     for j in range(ma):
       cu[i, j] = fit_fos[j](xi)*tmp
     b[i] = y[i]*tmp

   u, w, v = numpy.linalg.svd(cu, 0)
   wmax = numpy.max(w)
   threshold = tol*wmax
   for j in range(ma):
     if w[j] < threshold:
       w[j] = 0.0
   a = singular_value_decomposition_back_substitution(u, w, v, b)
   return a


def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()

   
