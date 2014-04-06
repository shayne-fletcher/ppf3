from ppf.math import semi_analytic_domain_integrator

class rollback(object):
  def __init__(self, ccy):
     self.__ccy = ccy
     self.__integrator = semi_analytic_domain_integrator() 

  def rollback(self, t, T, state, req, env, yT):
     '''
     >>> import math
     >>> from ppf.math.interpolation import loglinear
     >>> times = [0.0, 0.5, 1.0, 1.5, 2.0]
     >>> factors = [math.exp(-0.05*t) for t in times]
     >>> import ppf.market
     >>> c = ppf.market.curve(times, factors, loglinear)
     >>> from numpy import zeros
     >>> expiries = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
     >>> tenors = [0, 90]
     >>> values = zeros((8, 2))
     >>> for i in range(8): values[i, 0] = 0.04
     >>> for i in range(8): values[i, 1] = 0.04
     >>> surf = ppf.market.surface(expiries, tenors, values)
     >>> env = ppf.market.environment()
     >>> key = "zc.disc.eur"
     >>> env.add_curve(key, c)
     >>> key = "ve.term.eur.hw"
     >>> env.add_surface(key, surf)
     >>> key = "cv.mr.eur.hw"
     >>> env.add_constant(key, 0.01)
     >>> r = ppf.model.hull_white.requestor()
     >>> s = ppf.model.hull_white.lattice.state("eur", 21, 3.5)
     >>> sx = s.fill(1.0, r, env)
     >>> f = ppf.model.hull_white.fill(2.0)
     >>> PtT = f.numeraire_rebased_bond(1.0, 1.5, "eur", env, r, sx)
     >>> roll = rollback("eur")
     >>> yt = roll.rollback(0.5, 1.0, s, r, env, PtT)
     >>> y0 = roll.rollback(0.0, 0.5, s, r, env, yt)
     >>> for i in range(21): print y0[i]
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     0.922022844448
     '''
     xt = state.fill(t, req, env)
     xT = state.fill(T, req, env)
     xtT = state.incremental_fill(t, T, req, env)
     ftT = state.incremental_distribution(t, T, req, env)
     return self.__integrator.rollback(t, T, xt, xT, xtT, ftT, yT)

  def rollback_max(self, t, T, state, req, env, yT):
     xt = state.fill(t, req, env)
     xT = state.fill(T, req, env)
     xtT = state.incremental_fill(t, T, req, env)
     ftT = state.incremental_distribution(t, T, req, env)
     return self.__integrator.rollback_max(t, T, xt, xT, xtT, ftT, yT)


def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
    
