from ppf.date_time import year_fraction
from ppf.date_time.day_count_basis import day_count_basis_strings

class flow(object):
  def __init__(self
             , notional
             , pay_currency
             , accrual_start_date
             , accrual_end_date
             , accrual_basis
             , pay_date
             , observables = None):
    self.__notional = notional
    self.__pay_currency = pay_currency
    self.__accrual_start_date = accrual_start_date
    self.__accrual_end_date = accrual_end_date
    self.__accrual_basis = accrual_basis
    self.__pay_date = pay_date
    self.__observables = observables

  def notional(self): return self.__notional
  def pay_currency(self): return self.__pay_currency
  def accrual_start_date(self): return self.__accrual_start_date
  def accrual_end_date(self): return self.__accrual_end_date
  def pay_date(self): return self.__pay_date
  def observables(self): return self.__observables
  def set_observables(self, observables): self.__observables = observables

  def year_fraction(self):
    return year_fraction(
        self.__accrual_start_date
      , self.__accrual_end_date
      , self.__accrual_basis)

  def __str__(self):
    s = "%f, " % self.__notional
    s += "%s, " % self.__pay_currency
    s += "[%s, %s], " % (self.__accrual_start_date, self.__accrual_end_date)
    s += "%s, " % day_count_basis_strings[self.__accrual_basis]
    s += "%s, " %  self.__pay_date
    if self.__observables != None:
      for observable in self.__observables:
        s += observable.__str__()
    return s
