import math
import ppf.market

class requestor(object):
  def discount_factor(self, t, ccy, env):
     '''
     >>> from ppf.math.interpolation import loglinear
     >>> times = [0.0, 0.5, 1.0, 1.5, 2.0]
     >>> factors = [math.exp(-0.05*t) for t in times]
     >>> c = ppf.market.curve(times, factors, loglinear)
     >>> env = ppf.market.environment()
     >>> key = "zc.disc.eur"
     >>> env.add_curve(key, c)
     >>> r = requestor()
     >>> t = 1.5
     >>> print r.discount_factor(t, "eur", env)
     0.927743486329
     '''
     key = "zc.disc."+ccy
     curve = env.retrieve_curve(key)
     return curve(t)

  def term_vol(self, t, ccy, env):
     '''
     >>> from numpy import zeros
     >>> expiries = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
     >>> tenors = [0, 90]
     >>> values = zeros((8, 2))
     >>> for i in range(8): values[i, 0] = 0.04
     >>> for i in range(8): values[i, 1] = 0.04
     >>> surf = ppf.market.surface(expiries, tenors, values)
     >>> env = ppf.market.environment()
     >>> key = "ve.term.eur.hw"
     >>> env.add_surface(key, surf)
     >>> key = "cv.mr.eur.hw"
     >>> env.add_constant(key, 0.0)
     >>> r = requestor()
     >>> t = 0.25
     >>> print r.term_vol(t, "eur", env)
     0.1
     '''
     key = "ve.term."+ccy+".hw"
     surf = env.retrieve_surface(key)
     termt = surf(t, 0)
     key = "cv.mr."+ccy+".hw"
     mr = env.retrieve_constant(key)
     term_var = termt
     if mr <> 0:
       term_var *= (math.exp(2.0*mr*t)-1.0)/(2.0*mr)
     else:
       term_var *= t
     return math.sqrt(term_var)

  def local_vol(self, t, T, ccy, env):
     assert t <= T
     key = "cv.mr."+ccy+".hw"
     mr = env.retrieve_constant(key)
     if mr <> 0:
       return (math.exp(-mr*t)-math.exp(-mr*T))/mr
     else:
       return T-t

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
    
