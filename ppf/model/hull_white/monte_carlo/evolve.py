import math
import random

class evolve(object):
  def __init__(self, ccy, seed = 1234, antithetic = True):
     self.__ccy = ccy
     self.__seed = seed
     self.__antithetic = antithetic

  def evolve(self, t, T, state, req, env):
     '''
     >>> import ppf.market
     >>> from numpy import zeros
     >>> expiries = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
     >>> tenors = [0, 90]
     >>> values = zeros((8, 2))
     >>> values.fill(0.01)
     >>> surf = ppf.market.surface(expiries, tenors, values)
     >>> env = ppf.market.environment()
     >>> key = "ve.term.eur.hw"
     >>> env.add_surface(key, surf)
     >>> key = "cv.mr.eur.hw"
     >>> env.add_constant(key, 0.01)
     >>> r = ppf.model.hull_white.requestor()
     >>> s = ppf.model.hull_white.monte_carlo.state(10000)
     >>> e = evolve("eur")
     >>> e.evolve(0.0,0.5,s,r,env)
     >>> e.evolve(0.5,1.0,s,r,env)
     >>> variates = s.get_variates()
     >>> mean = variates.sum()/10000
     >>> print math.fabs(mean) < 1.0e-4
     True
     >>> tmp = variates*variates
     >>> variance = tmp.sum()/10000
     >>> vol = r.term_vol(1.0,"eur",env)
     >>> print math.fabs(variance-vol*vol) < 1.0e-4
     True
     '''
     if t > T:
       raise RuntimeError, 'attempting to evolve backwards'
     if t == T:
       return
     variates = state.get_variates()
     num_sims = variates.shape[0]
     if self.__antithetic:
       if num_sims%2 <> 0:
         raise RuntimeError, \
           'expected number of simulations to be even with antithetic'
       num_sims /= 2
     volt = req.term_vol(t, self.__ccy, env)
     volT = req.term_vol(T, self.__ccy, env)
     vartT = volT*volT-volt*volt
     if vartT < 0:
       raise RuntimeError, 'negative incremental variance'
     voltT = math.sqrt(vartT)
     generator = random.Random(self.__seed)
     for i in range(num_sims):
       z = generator.gauss(0, 1.0)
       variates[i] = variates[i]+voltT*z
       if self.__antithetic:
         variates[num_sims+i] = variates[num_sims+i]-voltT*z
     state.set_variates(variates)
     self.__seed = self.__seed+1

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
