from fixing import *
from observable import *
from generate_flows import *
from generate_observables import *

class swap_rate(observable):
  def __init__(self
             , attributes
             , flow_id
             , reset_id
             , reset_date
             , reset_ccy
             , proj_start_date
             , proj_end_date
             , fix
             , spread=None):
    observable.__init__(self
                      , attributes
                      , flow_id
                      , reset_id
                      , reset_ccy
                      , reset_date
                      , proj_end_date
                      , fix
                      , spread)
    self.__proj_start_date = proj_start_date
    self.__proj_end_date = proj_end_date
    self.__generate()

  def proj_start_date(self): return self.__proj_start_date
  def proj_end_date(self): return self.__proj_end_date
  def fixed_pay_basis(self) : return self.__fixed_pay_basis
  def float_pay_basis(self) : return self.__float_pay_basis
  def proj_basis(self): return self.__proj_basis
  def fixed_flows(self): return self.__fixed_flows
  def float_flows(self): return self.__float_flows

  def __str__(self):
    s = "%d, " % self.flow_id()
    s += "%d, " % self.reset_id()
    s += "%s, " % self.reset_currency()
    s += "[%s, %s], " % (self.__proj_start_date, self.__proj_end_date)
    return s

  def __generate(self):
    start = self.__proj_start_date
    until = self.__proj_end_date
    attributes = self.attributes()

    fixed_period = attributes["fixed-pay-period"]
    fixed_period_duration = attributes["fixed-pay-period-duration"]
    fixed_pay_basis = attributes["fixed-pay-basis"]
    fixed_pay_holiday_centers = attributes["fixed-pay-holiday-centers"]
    fixed_shift_convention = attributes["fixed-shift-convention"]

    float_period = attributes["float-pay-period"]
    float_period_duration = attributes["float-pay-period-duration"]
    float_pay_basis = attributes["float-pay-basis"]
    float_pay_holiday_centers = attributes["float-pay-holiday-centers"]
    float_shift_convention = attributes["float-shift-convention"]

    libor_basis = attributes["index-basis"]
    libor_holiday_centers = attributes["index-holiday-centers"]
    libor_shift_convention = attributes["index-shift-convention"]

    self.__fixed_flows = \
       generate_flows(start
                    , until
                    , period = fixed_period
                    , duration = fixed_period_duration
                    , pay_shift_method = fixed_shift_convention
                    , pay_currency = self.reset_currency()
                    , pay_basis = fixed_pay_basis
                    , pay_holiday_centers = fixed_pay_holiday_centers
                    , accrual_shift_method = fixed_shift_convention
                    , accrual_holiday_centers = fixed_pay_holiday_centers)
    libor_observables = \
       generate_libor_observables(
                      start
                    , until
                    , roll_period = float_period
                    , roll_duration = float_period_duration
                    , reset_period = float_period
                    , reset_duration = float_period_duration
                    , tenor_period = float_period
                    , tenor_duration = float_period_duration
                    , reset_currency = self.reset_currency()
                    , reset_basis = libor_basis
                    , reset_holiday_centres = libor_holiday_centers
                    , reset_shift_method = libor_shift_convention)
    self.__float_flows = \
       generate_flows(start
                    , until
                    , period = float_period
                    , duration = float_period_duration
                    , pay_shift_method = float_shift_convention
                    , pay_currency = self.reset_currency()
                    , pay_basis = float_pay_basis
                    , pay_holiday_centers = float_pay_holiday_centers
                    , accrual_shift_method = float_shift_convention
                    , accrual_holiday_centers = float_pay_holiday_centers
                    , observables = libor_observables)

  def forward(self, t, curve):
    fund_pv = 0
    for f in self.__float_flows:
      obs = f.observables()[0]
      proj_start, proj_end, reset_accrual_dcf = \
           (obs.proj_start_date(), obs.proj_end_date(), obs.year_fraction())
      dfs, dfe = \
           curve(int(proj_start - t)/365.0), curve(int(proj_end - t)/365.0)
      libor = (dfs/dfe - 1.0)/reset_accrual_dcf
      pay_date, accrual_dcf = (f.pay_date(), f.year_fraction())
      dfp = curve(int(pay_date - t)/365.0)
      fund_pv += dfp*libor*accrual_dcf

    fixed_pv = 0
    for f in self.__fixed_flows:
      pay_date, accrual_dcf = (f.pay_date(), f.year_fraction())
      dfp = curve(int(pay_date - t)/365.0)
      fixed_pv += dfp*accrual_dcf

    return fund_pv/fixed_pv

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()
