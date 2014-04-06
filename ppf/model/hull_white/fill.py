import math
import numpy
from ppf.date_time import year_fraction
import ppf.market
from ppf.core import libor_rate
from ppf.core import swap_rate

class fill(object):
  def __init__(self, terminal_T):
     self.__terminal_T = terminal_T

  def numeraire_rebased_bond(self, t, T, ccy, env, requestor, state):
     '''
     >>> from ppf.math.interpolation import loglinear
     >>> times = [0.0, 0.5, 1.0, 1.5, 2.0]
     >>> factors = [math.exp(-0.05*t) for t in times]
     >>> c = ppf.market.curve(times, factors, loglinear)
     >>> expiries = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
     >>> tenors = [0, 90]
     >>> values = numpy.zeros((8, 2))
     >>> for i in range(8): values[i, 0] = 0.0
     >>> for i in range(8): values[i, 1] = 0.0
     >>> surf = ppf.market.surface(expiries, tenors, values)
     >>> env = ppf.market.environment()
     >>> key = "zc.disc.eur"
     >>> env.add_curve(key, c)
     >>> key = "ve.term.eur.hw"
     >>> env.add_surface(key, surf)
     >>> key = "cv.mr.eur.hw"
     >>> env.add_constant(key, 0.0)
     >>> r = ppf.model.hull_white.requestor()
     >>> s = ppf.model.hull_white.lattice.state("eur", 11, 3.5)
     >>> sx = s.fill(0.25, r, env)
     >>> f = fill(2.0)
     >>> PtT = f.numeraire_rebased_bond(0.25, 1.5, "eur", env, r, sx)
     >>> for i in range(11): print PtT[i]
     0.927743486329
     0.927743486329
     0.927743486329
     0.927743486329
     0.927743486329
     0.927743486329
     0.927743486329
     0.927743486329
     0.927743486329
     0.927743486329
     0.927743486329
     '''
     if t > T:
       raise RuntimeError, 'time beyond maturity of bond'
     if T > self.__terminal_T:
       raise RuntimeError, 'bond maturity after terminal measure bond maturity'
     if len(state.shape) <>1:
       raise RuntimeError, 'expected one dimensional arrays'
     dfTN = 1.0 #numeraire scaled to unit
     dfT = requestor.discount_factor(T, ccy, env)
     gt = requestor.term_vol(t, ccy, env)
     phiTTN = requestor.local_vol(T, self.__terminal_T, ccy, env)
     scale = dfT/dfTN*math.exp(-0.5*gt*gt*phiTTN*phiTTN) 
     n = state.shape[0]
     ret = numpy.zeros(n)
     for i in range(n):
        x = state[i]
        ret[i] = scale*math.exp(phiTTN*x)
     return ret

  def numeraire(self, t, ccy, env, requestor, state):
     if t > self.__terminal_T:
       raise RuntimeError, 'time beyond terminal measure bond maturity'
     ptt = self.numeraire_rebased_bond(t, t, ccy, env, requestor, state)
     n = state.shape[0]
     ret = numpy.zeros(n)
     ret.fill(1.0)
     ret = ret/ptt
     return ret

  def libor(self, t, libor_obs, env, requestor, state):
     '''
     >>> from ppf.math.interpolation import loglinear
     >>> times = [0.0, 0.5, 1.0, 1.5, 2.0]
     >>> factors = [math.exp(-0.05*t) for t in times]
     >>> c = ppf.market.curve(times, factors, loglinear)
     >>> expiries = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
     >>> tenors = [0, 90]
     >>> values = numpy.zeros((8, 2))
     >>> for i in range(8): values[i, 0] = 0.0
     >>> for i in range(8): values[i, 1] = 0.0
     >>> surf = ppf.market.surface(expiries, tenors, values)
     >>> from ppf.date_time import *
     >>> pd = date(2008, 01, 01)
     >>> env = ppf.market.environment(pd)
     >>> key = "zc.disc.eur"
     >>> env.add_curve(key, c)
     >>> key = "ve.term.eur.hw"
     >>> env.add_surface(key, surf)
     >>> key = "cv.mr.eur.hw"
     >>> env.add_constant(key, 0.0)
     >>> rd = date(2008, 07, 01)
     >>> libor_obs = ppf.core.libor_rate(None, 0, 0, rd, "eur",\
         rd, shift(rd+months(6), modified_following),\
         basis_act_360, ppf.core.fixing(False))
     >>> r = ppf.model.hull_white.requestor()
     >>> s = ppf.model.hull_white.lattice.state("eur", 11, 3.5)
     >>> sx = s.fill(0.25, r, env)
     >>> f = fill(2.0)
     >>> libortT = f.libor(0.25, libor_obs, env, r, sx)
     >>> for i in range(11): print libortT[i]
     0.0499418283138
     0.0499418283138
     0.0499418283138
     0.0499418283138
     0.0499418283138
     0.0499418283138
     0.0499418283138
     0.0499418283138
     0.0499418283138
     0.0499418283138
     0.0499418283138
     '''
     if len(state.shape) <>1:
       raise RuntimeError, 'expected one dimensional array'
     n = state.shape[0]
     fix = libor_obs.fix()
     if fix.is_fixed():
       ret = numpy.zeros(n)
       for i in range(n):
          ret[i] = fix.value()
       return ret

     proj_start_date = libor_obs.proj_start_date()
     proj_end_date = libor_obs.proj_end_date()
     dcf = libor_obs.year_fraction()
     dfs = self.numeraire_rebased_bond(t, env.relative_date(proj_start_date)/365.0,\
                                       libor_obs.reset_currency(), env, requestor, state)
     dfe = self.numeraire_rebased_bond(t, env.relative_date(proj_end_date)/365.0,\
                                       libor_obs.reset_currency(), env, requestor, state)
     ret = numpy.zeros(n)
     for i in range(n):
        ret[i] = (dfs[i]/dfe[i]-1.0)/dcf
     return ret

  def swap(self, t, swap_obs, env, requestor, state):
     if len(state.shape) <> 1:
       raise RuntimeError, 'expected one dimensional array'
     n = state.shape[0]
     fix = swap_obs.fix()
     if fix.is_fixed():
       ret = numpy.zeros(n)
       for i in range(n):
          ret[i] = fix.value()
       return ret

     fixed_flows = swap_obs.fixed_flows()
     fixed_pv = numpy.zeros(n)
     for f in fixed_flows:
        pay_date, dcf = \
          (f.pay_date(), f.year_fraction())
        dfp = self.numeraire_rebased_bond(t, pay_date, swap_obs.reset_currency(), env, requestor, state)
        for i in range(n):
           fixed_pv[i] += dcf*dfp[i]
     float_flows = swap_obs.float_flows()
     float_pv = numpy.zeros(n)
     for f in float_flows:
        obs = f.observables()[0]
        proj_start, proj_end, reset_dcf = \
                   (obs.proj_start_date(), obs.proj_end_date(), obs.year_fraction())
        dfs = self.numeraire_rebased_bond(t, proj_start,\
              swap_obs.reset_currency(), env,\
              requestor, state)
        dfe = self.numeraire_rebased_bond(t, proj_end,\
              swap_obs.reset_currency(), env,\
              requestor, state)
        pay_date, dcf = \
          (f.pay_date(), f.year_fraction())
        dfp = self.numeraire_rebased_bond(t, pay_date,\
               swap_obs.reset_currency(), env,\
               requestor, state)
        for i in range(n):
           float_pv[i] += (dfs[i]/dfe[i]-1.0)/reset_dcf*dcf*dfp[i]
     ret = numpy.zeros(n)
     for i in range(n):
        ret[i] = float_pv[i]/fixed_pv[i]
     return ret
    
def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
            
