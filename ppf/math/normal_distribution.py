import math
import numpy
import ppf.utility
from .quadratic_roots import *
from .cubic_roots import *
from .special_functions import *
 
class normal_distribution(object):
  def __init__(self, mean=0.0, vol=1.0):
    self.mean = mean
    self.vol = vol
    if vol < 0.0:
      raise RuntimeError ('negative volatility')
    if vol != 0.0:
      self.vol_inv = 1.0/vol
    else:
      self.vol_inv = 1.0;
    self.unit_norm = 1.0/math.sqrt(2.0*math.pi)

  def unit_pdf(self, x):
    return math.exp(-0.5*x*x)*self.unit_norm
       
  def pdf(self, x):
    y = x*self.vol_inv
    return self.unit_pdf(y)*self.vol_inv
 
  def unit_cdf(self, x):
    return N(x)
    
  def cdf(self, x):
    '''
    >>> mean = 0.05
    >>> vol = 0.1
    >>> f = normal_distribution(mean, vol)
    >>> print f.cdf(mean)
    0.500000015
    >>> print f.cdf(100000)
    1.0
    '''        
    y = (x-self.mean)*self.vol_inv
    return self.unit_cdf(y)

  def __bounds_(self, cs, xl, xh):
    # cubic coefficients
    n = len(cs)
    a = 0
    b = 0
    c = 0
    d = 0
    if n >= 1:
      d = cs[0]
    if n >= 2:
      c = cs[1]
    if n >= 3:
      b = cs[2]
    if n == 4:
      a = cs[3]
    if n > 4:
      raise RuntimeError ('can only handle up to cubics')
    # roots
    roots = cubic_roots(a, b, c, d, xl, xh)
    bounds = []
    # calculate bounds
    xprev = xl
    for root in roots:
      xcurr = root
      xmid = 0.5*(xprev+xcurr)
      if d+xmid*(c+xmid*(b+xmid*a)) > 0:
        bounds.append([xprev, xcurr])
      xprev = xcurr
    xcurr = xh      
    xmid = 0.5*(xprev+xcurr)
    if d+xmid*(c+xmid*(b+xmid*a)) > 0:
      bounds.append([xprev, xcurr])
    return bounds

  def regrid(self, xs, cs, regrid_xs):
    '''
    >>> mean = 0.05
    >>> vol = 0.1
    >>> f = normal_distribution(mean, vol)
    >>> xs = f.state(4.5, 10)
    >>> cs = numpy.zeros((4,6))
    >>> for i in range(6): cs[:, i] = 1.0, 0.0, 1.0, 0.0
    >>> regrid_fs = f.regrid(xs, cs, xs)
    >>> for i in range(2, 8): print "%f, %f" % (regrid_fs[i], cs[0,i-2]+xs[i]*(cs[1,i-2]+xs[i]*(cs[2,i-2]+xs[i]*cs[3,i-2]))) 
    1.040000, 1.040000
    1.010000, 1.010000
    1.000000, 1.000000
    1.010000, 1.010000
    1.040000, 1.040000
    1.090000, 1.090000
    '''
    m = len(xs)
    n = len(regrid_xs)
    # regrid function
    regrid_fs = numpy.zeros(n)
    for i in range(n):
      x = regrid_xs[i]
      # bound
      left, right = ppf.utility.equal_range(x, xs)
      if right == m: right -= 1
      if left == right: left -= 1
      idx = left
      # saturate
      if idx < 2: idx = 2
      if idx > m-3: idx = m-3
      csi = cs[:, idx-2]
      regrid_fs[i] = csi[0]+x*(csi[1]+x*(csi[2]+x*csi[3]))
    return regrid_fs 
    
  def moments(self, n, x):
    ys = (n)*[0.0]
    ys[0] = self.cdf(x)
    if n > 1:
      vol2 = self.vol*self.vol
      pdfx = self.pdf(x)
      ys[1] = -vol2*pdfx+self.mean*ys[0]
      xn = x
      for i in range(2, n):
         ys[i] = vol2*(-xn*pdfx+(i-1)*ys[i-2])+self.mean*ys[i-1]
         xn = xn*x
    return ys
        
  def integral(self, cs, xl, xh, yls = None, yhs = None):
    '''
    >>> mean = 0.05
    >>> vol = 0.1
    >>> f = normal_distribution(mean, vol)
    >>> cs = [1.0]
    >>> print f.integral(cs, -10000, 10000)
    1.0
    >>> cs = [0.0,1.0]
    >>> print f.integral(cs, -10000, 10000)
    0.05
    >>> cs = [0.0,0.0,1.0]
    >>> print f.integral(cs, -10000, 10000)
    0.0125
    '''
    if xl > xh:
      raise RuntimeError ('lower bound greater than upper bound of integration domain')
    n = len(cs)
    if yls == None:
      yls = self.moments(n, xl)
    else:
      if len(yls) != n:
        raise RuntimeError ("number of moments doesn't match number of coefficients")
    if yhs == None:
      yhs = self.moments(n, xh)
    else:
      if len(yhs) != n:
        raise RuntimeError ("number of moments doesn't match number of coefficients")
    sum = 0.0
    for i in range(n):
      sum += cs[i]*(yhs[i]-yls[i])
    return sum

  def integral_indicator(self, cs, indicator, xl, xh, yls = None, yhs = None):
    '''
    >>> mean = 0.05
    >>> vol = 0.1
    >>> f = normal_distribution(mean, vol)
    >>> yls = f.moments(4, -1)
    >>> yhs = f.moments(4, 10000)
    >>> cs = [0.0,0.0,1.0,1.0]
    >>> print f.integral_indicator(cs, cs, -10000, 10000)
    0.014125
    >>> print cs[2]*(yhs[2]-yls[2])+cs[3]*(yhs[3]-yls[3])
    0.014125
    '''
    if xl > xh:
      raise RuntimeError ('lower bound greater than upper bound of integration domain')
        
    bounds = self.__bounds_(indicator, xl, xh)
    sum = 0
    for bound in bounds:
       xll = bound[0]
       xrr = bound[1]
       yll = None
       yrr = None
       if xll == xl:
         yll = yls
       if xrr == xh:
         yrr = yhs
       sum += self.integral(cs, xll, xrr, yll, yrr)
    return sum

  def integral_max(self, cs, xl, xh, yls = None, yhs = None):
    '''
    >>> mean = 0.05
    >>> vol = 0.1
    >>> f = normal_distribution(mean, vol)
    >>> yls = f.moments(4, -1)
    >>> yhs = f.moments(4, 10000)
    >>> cs = [0.0,0.0,1.0,1.0]
    >>> print f.integral_max(cs, -10000, 10000)
    0.014125
    >>> print cs[2]*(yhs[2]-yls[2])+cs[3]*(yhs[3]-yls[3])
    0.014125
    '''
    if xl > xh:
      raise RuntimeError ('lower bound greater than upper bound of integration domain')
        
    return self.integral_indicator(cs, cs, xl, xh, yls, yhs)


  def state(self, stddev, n):
    if n < 2:
      raise RuntimeError ('number of points must be greater than one')
    s = numpy.zeros(n)
    dx = 2*stddev/(n-1)
    for i in range(n):
       s[i] = self.mean+self.vol*(-stddev+i*dx)
    return s
        
def  _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
    
