import numpy
from ppf.core import *

class cle_exercise(object):
  def __init__(self, l):
    self.__leg = l
  def num_explanatory_variables(self):
    return 2
  def __call__(self, t, fill, state, requestor, env):
    '''
    >>> from ppf.math.interpolation import loglinear
    >>> times = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    >>> import math
    >>> factors = [math.exp(-0.05*t) for t in times]
    >>> c = ppf.market.curve(times, factors, loglinear)
    >>> expiries = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
    >>> tenors = [0, 90]
    >>> values = numpy.zeros((8, 2))
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
    >>> r = ppf.model.hull_white.requestor()
    >>> s = ppf.model.hull_white.monte_carlo.state(10)
    >>> sx = s.fill(0.25, r, env)
    >>> f = ppf.model.hull_white.fill(3.0)
    >>> flows = generate_flows(
    ...   start  = date(2008, 01, 01)
    ...   , end  = date(2010, 01, 01)
    ...   , resolution = date_resolutions.months
    ...   , period = 6
    ...   , shift_method = shift_convention.modified_following
    ...   , basis = "ACT/360"
    ...   , pay_currency = "EUR")
    >>> lg = leg(flows, PAY)
    >>> ex = cle_exercise(lg)
    >>> t = env.relative_date(flows[1].accrual_start_date())/365.0
    >>> T = env.relative_date(flows[1].accrual_end_date())/365.0
    >>> ret = ex(t, f, sx, r, env)
    >>> dft = c(t)
    >>> dfT = c(T)
    >>> libor = (dft/dfT-1.0)/flows[1].year_fraction()
    >>> pv01 = 0.0
    >>> for fl in flows[1:]:
    ...   T = env.relative_date(fl.pay_date())/365.0
    ...   dfT = c(T)
    ...   pv01 += fl.year_fraction()*dfT
    >>> T = env.relative_date(flows[-1].accrual_end_date())/365.0
    >>> dfT = c(T)
    >>> swap = (dft-dfT)/pv01
    >>> libors = ret[:, 0]
    >>> swaps = ret[:, 1]
    >>> for rate in libors:
    ...   print rate == libor
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    >>> for rate in swaps:
    ...   print rate == swap
    True
    True
    True
    True
    True
    True
    True
    True
    True
    True
    '''
    # harvest active flows
    all_flows = self.__leg.flows()
    flows = []
    for flow in all_flows:
      accrual_start_days = env.relative_date(flow.accrual_start_date())
      if accrual_start_days >= t*365.0:
        flows.append(flow)
    if len(flows) < 1:
      raise RuntimeError, "no active flows remainning"

    # explanatory variables
    num_sims = state.shape[0]
    evs = numpy.zeros((num_sims, self.num_explanatory_variables()))
    pv01 = numpy.zeros(num_sims)
    notl_exchange = numpy.zeros(num_sims)
    cnt = 0 
    for flow in flows:
      Ts = env.relative_date(flow.accrual_start_date())/365.0        
      Te = env.relative_date(flow.accrual_end_date())/365.0        
      Tp = env.relative_date(flow.pay_date())/365.0
      dfp = fill.numeraire_rebased_bond(t, Tp, flow.pay_currency(), env, requestor, state)
      pv01 += flow.year_fraction()*dfp
      if cnt == 0:
        dfs = fill.numeraire_rebased_bond(t, Ts, flow.pay_currency(), env, requestor, state)
        notl_exchange = dfs
        dfe = fill.numeraire_rebased_bond(t, Te, flow.pay_currency(), env, requestor, state)
        evs[:, 0] = (dfs/dfe-1.0)/flow.year_fraction()
      elif cnt == len(flows)-1:
        notl_exchange -= fill.numeraire_rebased_bond(t, Te, flow.pay_currency(), env, requestor, state)
      cnt = cnt+1 
      
    evs[:, 1] = notl_exchange/pv01

    return evs

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
            
