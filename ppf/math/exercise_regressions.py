import numpy
from generalised_least_squares import *

# max for numpy arrays
max_ = numpy.vectorize(lambda x, y: (x, y)[x < y])

class unit_fo(object):
  def __call__(self, x):
    return 1.0
class linear_fo(object):
  def __init__(self, i):
    self.__i = i
  def __call__(self, x):
    return x[self.__i]
class quadratic_fo(object):
  def __init__(self, i, j):
    self.__i = i
    self.__j = j
  def __call__(self, x):
    return x[self.__i]*x[self.__j]

class n_quadratic_fo(object):
  def __init__(self,num_expl_vars):
    self.__fos = []
    self.__fos.append(unit_fo())
    for i in range(num_expl_vars):
      self.__fos.append(linear_fo(i))
      for j in range(i, num_expl_vars):
        self.__fos.append(quadratic_fo(i, j))
    self.__n = len(self.__fos)
  def __call__(self, alphas, x):
    y = 0.0
    for i in range(self.__n):
      y += alphas[i]*self.__fos[i](x)
    return y
  def fit_fos(self):
    return self.__fos
   
class fitted_fo(object):
  def __init__(self, alphas, fo):
    self.__alphas = alphas
    self.__fo = fo
  def __call__(self, x):
    return self.__fo(self.__alphas, x)

def fit(x, y):
  if len(x.shape) <> 2:
    raise RuntimeError, "Expected 'x' to be 2d array"
  if len(y.shape) <> 1:
    raise RuntimeError, "Expected 'y' to be 1d array"
  num_obs = x.shape[0]
  num_expl_vars = x.shape[1]
  if num_obs <> y.shape[0]:
    raise RuntimeError, "'y' array has wrong size"

  fo = n_quadratic_fo(num_expl_vars)
  sig = numpy.zeros(num_obs)  
  sig.fill(1.0)
  alphas = generalised_least_squares_fit(y, x, sig, fo.fit_fos())
  return fitted_fo(alphas, fo)

def evaluate_regression(x, fo):
  if len(x.shape) <> 2:
    raise RuntimeError, "Expected 'x' to be a 2d array"
  num_obs = x.shape[0]
  y = numpy.zeros(num_obs)
  for i in range(num_obs):
    y[i] = fo(x[i, :])
  return y

def pickup_value_regression(ies, ns, vs):
  if len(ies.shape) <> 2:
    raise RuntimeError, "Expected 'immediate exercise values' to be a 2d array"
  if len(ns.shape) <> 2:
    raise RuntimeError, "Expected 'numeraires' to be a 2d array"
  if len(vs.shape) <> 3:
    raise RuntimeError, "Expected 'explanatory variables' to be a 3d array"

  num_times = ies.shape[0]
  num_obs = ies.shape[1]
  num_expl_vars = vs.shape[2]

  if ns.shape[0] <> num_times or ns.shape[1] <> num_obs:
    raise RuntimeError, "'numeraires' array has wrong size"
  if vs.shape[0] <> num_times or vs.shape[1] <> num_obs:
    raise RuntimeError, "'explanatory variables' array has wrong size"

  fitted_fos = []
  zero = numpy.zeros(num_obs)
  H = numpy.zeros(num_obs) # holding value
  for i in range(num_times-1,-1,-1):
    x = vs[i, :, :]
    n = ns[i, :]
    pv = n*(ies[i, :]-H) # reinflate by numeraire
    fit_fo = fit(x, pv)
    temp = evaluate_regression(x, fit_fo) # pickup value regression
    fitted_fos.insert(0, fit_fo)
    H += max_(temp/n, zero) # deflate by numeraire

  return fitted_fos


