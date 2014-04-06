import math

from .piecewise_polynomial_fitting import *
from .normal_distribution import *

class semi_analytic_domain_integrator(object):

  def __create_cached_moments(self, x, f):
    n = x.shape[0]
    self.__ys = numpy.zeros([n, 4])
    self.__ys[2] = f.moments(4, x[2]) # cubic
    for j in range(2, n-2):
      self.__ys[j+1] = f.moments(4, x[j+1]) # cubic

  def __rollback_(self, t, T, xt, xT, xtT, yT, regridder, integrator):
    if len(xt.shape) != len(xT.shape) or \
       len(xT.shape) != len(yT.shape) or \
       len(xt.shape) != 1 or len(xtT.shape) != 1:
      raise RuntimeError ('expected one dimensional arrays')

    nt = xt.shape[0]
    nT = xT.shape[0]
    ntT = xtT.shape[0]

    if nt != nT or ntT != nT:
      raise RuntimeError ('expected array to be of same size')

    if yT.shape[0] != nT:
      raise RuntimeError ('array yT has different number of points to xT')

    yt = numpy.zeros(nt)
    cT = piecewise_cubic_fit(xT, yT)
    for i in range(nt):
      # regrid
      regrid_xT = numpy.zeros(nT)
      xti = xt[i]
      for j in range(nT):
        regrid_xT[j] = xti+xtT[j]
      regrid_yT = regridder(xT, cT, regrid_xT)
      # polynomial fit
      cs = piecewise_cubic_fit(xtT, regrid_yT)
      # perform expectation
      sum = 0
      xl = xtT[2]
      for j in range(2, nT-2): # somehow this should be enscapsulated
        xh = xtT[j+1]
        sum = sum + integrator(cs[:, j-2], xl, xh, self.__ys[j], self.__ys[j+1])
        xl = xh
      yt[i] = sum
      if t == 0.0:
        for j in range(1, nt):
          yt[j] = yt[0]
        break

    return yt
    
  def rollback(self, t, T, xt, xT, xtT, ftT, yT):
    '''
    >>> integrator = semi_analytic_domain_integrator()
    >>> nt = 31
    >>> nT = 31
    >>> ntT = 31
    >>> t = 0.5
    >>> T = 1.0
    >>> mut = 0.0
    >>> muT = 0.0
    >>> vol = 0.2
    >>> volt = vol*math.sqrt(t)
    >>> volT = vol*math.sqrt(T)
    >>> ft = normal_distribution(mut, volt)
    >>> fT = normal_distribution(muT, volT)
    >>> xt = ft.state(5.5, nt)
    >>> xT = fT.state(5.5, nT)
    >>> meantT = muT-mut
    >>> voltT = math.sqrt(volT*volT-volt*volt)
    >>> ftT = normal_distribution(meantT, voltT)
    >>> xtT = ftT.state(5.5, ntT)
    >>> yT = numpy.zeros([nT])
    >>> for i in range(nT): yT[i] = math.exp(xT[i]-0.5*volT*volT) # lognormal martingale
    >>> yt = integrator.rollback(t, T, xt, xT, xtT, ftT, yT)
    >>> print "%f, %f" % (yt[15], math.exp(xt[15]-0.5*volt*volt))
    0.990049, 0.990050
    >>> ns = 31
    >>> nsT = 31
    >>> s = 0
    >>> mus = 0.0
    >>> vols = 0.0
    >>> fs = normal_distribution(mus, vols)
    >>> xs = fs.state(5.5, ns)
    >>> meansT = muT-mus
    >>> volsT = math.sqrt(volT*volT-vols*vols)
    >>> fsT = normal_distribution(meansT, volsT)
    >>> xsT = fsT.state(5.5, nsT)
    >>> ys = integrator.rollback(s, T, xs, xT, xsT, fsT, yT)
    >>> meanst = mut-mus
    >>> volst = math.sqrt(volt*volt-vols*vols)
    >>> fst = normal_distribution(meanst, volst)
    >>> nst = 31
    >>> xst = fst.state(5.5, nst)
    >>> ys1 = integrator.rollback(s, t, xs, xt, xst, fst, yt)
    >>> for i in range(ns): print "%f, %f" % (ys[i], ys1[i])
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    0.999999, 0.999999
    '''

    # create cache of moments
    self.__create_cached_moments(xtT, ftT)    

    return self.__rollback_(t, T, xt, xT, xtT, yT, ftT.regrid, ftT.integral)

  def rollback_max(self, t, T, xt, xT, xtT, ftT, yT):
    '''
    >>> integrator = semi_analytic_domain_integrator()
    >>> nT = 31
    >>> t = 0.5
    >>> T = 1.0
    >>> mut = 0.0
    >>> muT = 0.0
    >>> vol = 0.2
    >>> volt = vol*math.sqrt(t)
    >>> volT = vol*math.sqrt(T)
    >>> fT = normal_distribution(muT, volT)
    >>> xT = fT.state(5.5, nT)
    >>> yT = numpy.zeros([nT])
    >>> for i in range(nT): yT[i] = math.exp(xT[i]-0.5*volT*volT) # lognormal martingale
    >>> ns = 31
    >>> nsT = 31
    >>> s = 0
    >>> mus = 0.0
    >>> vols = 0.0
    >>> fs = normal_distribution(mus, vols)
    >>> xs = fs.state(5.5, ns)
    >>> meansT = muT-mus
    >>> volsT = math.sqrt(volT*volT-vols*vols)
    >>> fsT = normal_distribution(meansT, volsT)
    >>> xsT = fsT.state(5.5, nsT)
    >>> for i in range(nT): yT[i] -= 1.0 # strike 1.0
    >>> ys = integrator.rollback_max(s, T, xs, xT, xsT, fsT, yT)
    >>> d1 = 0.5*volT
    >>> for i in range(ns): print "%f, %f" % (ys[i], 2.0*fsT.unit_cdf(d1)-1.0)
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    0.079655, 0.079656
    '''

    # create cache of moments
    self.__create_cached_moments(xtT, ftT)    

    return self.__rollback_(t, T, xt, xT, xtT, yT, ftT.regrid, ftT.integral_max)

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
        
