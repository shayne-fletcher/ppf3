import math
import numpy
import ppf.market
from ppf.math.normal_distribution import *

class state:
  def __init__(self, ccy, n = 31, stddev = 5.5):
     self.__ccy = ccy
     self.__n = n
     self.__stddev = stddev

  def fill(self, t, req, env):
     '''
     >>> expiries = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
     >>> tenors = [0, 90]
     >>> from numpy import zeros
     >>> values = zeros((8, 2))
     >>> for i in range(8): values[i, 0] = 0.04
     >>> for i in range(8): values[i, 1] = 0.04
     >>> surf = ppf.market.surface(expiries, tenors, values)
     >>> env = ppf.market.environment()
     >>> key = "ve.term.eur.hw"
     >>> env.add_surface(key, surf)
     >>> key = "ve.local.eur.hw"
     >>> env.add_surface(key, surf)
     >>> key = "cv.mr.eur.hw"
     >>> env.add_constant(key, 0.01)
     >>> r = ppf.model.hull_white.requestor()
     >>> s = state("eur", 11, 3.5)
     >>> x = s.fill(1.25, r, env)
     >>> for i in range(11): print x[i]
     -0.787540762658
     -0.630032610127
     -0.472524457595
     -0.315016305063
     -0.157508152532
     0.0
     0.157508152532
     0.315016305063
     0.472524457595
     0.630032610127
     0.787540762658
     '''
     term_vol = req.term_vol(t, self.__ccy, env)
     f = normal_distribution(0, term_vol)
     return f.state(self.__stddev, self.__n)

  def __incremental_vol(self, t, T, req, env):
     term_volt = req.term_vol(t, self.__ccy, env)
     term_volT = req.term_vol(T, self.__ccy, env)
     term_vartT = term_volT*term_volT-term_volt*term_volt
     if term_vartT < 0:
       raise RuntimeError,\
         "incremental variance is negative"+" t = "+str(t)+" T = "+str(T)
     term_voltT = math.sqrt(term_vartT)
     return term_voltT      

  def incremental_fill(self, t, T, req, env):
     term_voltT = self.__incremental_vol(t, T, req, env)
     f = normal_distribution(0, term_voltT)     
     return f.state(self.__stddev, self.__n)

  def incremental_distribution(self, t, T, req, env):
     term_voltT = self.__incremental_vol(t, T, req, env)
     return normal_distribution(0, term_voltT)

  def create_variable(self):
     var = numpy.zeros(self.__n)
     return var  


def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
