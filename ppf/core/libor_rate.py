from ppf.date_time import year_fraction
from ppf.date_time.day_count_basis import day_count_basis_strings

from fixing import *
from observable import *

class libor_rate(observable):
  def __init__(self
             , attributes
             , flow_id
             , reset_id
             , reset_date
             , reset_currency
             , proj_start_date
             , proj_end_date
             , proj_basis
             , fix
             , spread=None):
    observable.__init__(self
                      , attributes
                      , flow_id
                      , reset_id
                      , reset_currency
                      , reset_date
                      , proj_end_date
                      , fix
                      , spread)
    self.__proj_start_date = proj_start_date
    self.__proj_end_date = proj_end_date
    self.__proj_basis = proj_basis

  def proj_start_date(self): return self.__proj_start_date
  def proj_end_date(self): return self.__proj_end_date
  def proj_basis(self): return self.__proj_basis

  def year_fraction(self):
    return year_fraction(self.__proj_start_date, self.__proj_end_date, self.__proj_basis)


  def forward(self, t, curve):
    '''
    >>> #rough discount factor curve
    >>> import math
    >>> from ppf.date_time import *
    >>> from ppf.math.interpolation import loglinear
    >>> t = date(2008, Jan, 7) #valuation date
    >>> times = range(0, 11)
    >>> P = loglinear(times, [math.exp(-0.05*T) for T in times])
    >>> for T in times: print "%d, %f" % (T, P(T))
    0, 1.000000
    1, 0.951229
    2, 0.904837
    3, 0.860708
    4, 0.818731
    5, 0.778801
    6, 0.740818
    7, 0.704688
    8, 0.670320
    9, 0.637628
    10, 0.606531
    >>> #construct a 3m libor forward
    >>> L = libor_rate(None, 0, 0, t, "JPY", \
        t, shift(t + months(3), modified_following), \
        basis_act_360, fixing(False))
    >>> print L.forward(t, P)
    0.0496237244447

    '''
    from ppf.date_time import year_fraction

    fix = self.fix()
    if fix.is_fixed():
      return fix.value()

    start = self.__proj_start_date
    end = self.__proj_end_date
    Ts, Te = (int(start - t)/365.0, int(end - t)/365.0)
    Ps, Pe = (curve(Ts), curve(Te))
    dcf = year_fraction(start, end, self.__proj_basis)
    forward = (Ps/Pe-1.0)/dcf

    return forward

  def __str__(self):
      s = "%d, " %  self.flow_id()
      s += "%d, " % self.reset_id()
      s += "%s, " % self.reset_currency()
      s += "[%s, %s], " % (self.__proj_start_date, self.__proj_end_date)
      s += "%s, " % day_count_basis_strings[self.__proj_basis]
      fix = self.fix()
      if fix.is_fixed():
         s += "%f, " % fix.value()
      spread = self.spread()
      if spread <> None:
         s += "%f, " % spread
      return s

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()
