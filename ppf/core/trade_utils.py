from ppf.date_time import *
from .trade import *
from .leg import *
from .flow import *

def final_important_date(trd):
  '''
  >>> from ppf.date_time import *
  >>> from pay_receive import *
  >>> from generate_flows import *
  >>> from generate_observables import *
  >>> from generate_exercise_table import *
  >>> from exercise_type import *
  >>> from leg import *
  >>> from trade import *
  >>> libor_observables = generate_libor_observables(
  ...     start  = date(2007, Jun, 29)
  ...   , end  = date(2009, Jun, 29)
  ...   , roll_period = 6
  ...   , roll_duration = ppf.date_time.months
  ...   , reset_period = 3
  ...   , reset_duration = ppf.date_time.months
  ...   , reset_currency = "JPY"
  ...   , reset_basis = basis_act_360
  ...   , reset_shift_method = shift_convention.modified_following)
  >>> coupon_observables = generate_fixed_coupon_observables(
  ...     start  = date(2007, Jun, 29)
  ...   , end  = date(2009, Jun, 29)
  ...   , roll_period = 6
  ...   , reset_currency = "JPY"
  ...   , coupon_shift_method = shift_convention.modified_following
  ...   , coupon_rate = 0.045)
  >>> #semi-annual flows
  >>> pay_flows = generate_flows(
  ...   start  = date(2007, Jun, 29)
  ...   , end  = date(2009, Jun, 29)
  ...   , duration = ppf.date_time.months
  ...   , period = 6
  ...   , shift_method = shift_convention.modified_following
  ...   , basis = "30/360"
  ...   , observables = coupon_observables)
  >>> rcv_flows = generate_flows(
  ...   start  = date(2007, Jun, 29)
  ...   , end  = date(2009, Jun, 29)
  ...   , duration = ppf.date_time.months
  ...   , period = 6
  ...   , shift_method = shift_convention.modified_following
  ...   , basis = "A/360"
  ...   , observables = libor_observables)
  >>> pay_leg = leg(pay_flows, PAY)
  >>> receive_leg = leg(rcv_flows, RECEIVE)
  >>> #1y nc
  >>> ex_sched = generate_exercise_table(
  ...   start = date(2008, Jun, 29)
  ... , end  = date(2009, Jun, 29)
  ... , period = 1
  ... , duration = ppf.date_time.years
  ... , shift_method = shift_convention.modified_following)
  >>> structure = trade((pay_leg, receive_leg), (ex_sched, exercise_type.callable))
  >>> print final_important_date(structure)  
  2009-Sep-29
  '''
  final_date = date(1900, Jan, 1)
  for l in trd.legs():
    for f in l.flows():
      candidate_date = f.pay_date()
      observables = f.observables()
      if not observables:
        raise RuntimeError ("Missing observables")
      for o in observables:
        if o.last_important_date() > candidate_date:
          candidate_date = o.last_important_date()
      if candidate_date > final_date:
        final_date = candidate_date
  return final_date

def enforce_single_currency(trd):
  '''
  >>> from ppf.date_time import *
  >>> from pay_receive import *
  >>> from generate_flows import *
  >>> from generate_observables import *
  >>> from generate_exercise_table import *
  >>> from exercise_type import *
  >>> from leg import *
  >>> from trade import *
  >>> libor_observables = generate_libor_observables(
  ...     start  = date(2007, Jun, 29)
  ...   , end  = date(2009, Jun, 29)
  ...   , roll_period = 6
  ...   , roll_duration = ppf.date_time.months
  ...   , reset_period = 3
  ...   , reset_duration = ppf.date_time.months
  ...   , reset_currency = "JPY"
  ...   , reset_basis = basis_act_360
  ...   , reset_shift_method = shift_convention.modified_following)
  >>> coupon_observables = generate_fixed_coupon_observables(
  ...     start  = date(2007, Jun, 29)
  ...   , end  = date(2009, Jun, 29)
  ...   , roll_period = 6
  ...   , reset_currency = "JPY"
  ...   , coupon_shift_method = shift_convention.modified_following
  ...   , coupon_rate = 0.045)
  >>> #semi-annual flows
  >>> pay_flows = generate_flows(
  ...   start  = date(2007, Jun, 29)
  ...   , end  = date(2009, Jun, 29)
  ...   , duration = ppf.date_time.months
  ...   , period = 6
  ...   , shift_method = shift_convention.modified_following
  ...   , basis = "30/360"
  ...   , pay_currency = "JPY"
  ...   , observables = coupon_observables)
  >>> rcv_flows = generate_flows(
  ...   start  = date(2007, Jun, 29)
  ...   , end  = date(2009, Jun, 29)
  ...   , duration = ppf.date_time.months
  ...   , period = 6
  ...   , shift_method = shift_convention.modified_following
  ...   , basis = "A/360"
  ...   , pay_currency = "JPY"
  ...   , observables = libor_observables)
  >>> pay_leg = leg(pay_flows, PAY)
  >>> receive_leg = leg(rcv_flows, RECEIVE)
  >>> #1y nc
  >>> ex_sched = generate_exercise_table(
  ...   start = date(2008, Jun, 29)
  ... , end  = date(2009, Jun, 29)
  ... , period = 1
  ... , duration = ppf.date_time.years
  ... , shift_method = shift_convention.modified_following)
  >>> structure = trade((pay_leg, receive_leg), (ex_sched, exercise_type.callable))
  >>> print enforce_single_currency(structure)  
  JPY
  '''
  ccys = []
  for l in trd.legs():
    for f in l.flows():
      pay_ccy = f.pay_currency()
      observables = f.observables()
      if not observables:
        raise RuntimeError ("Missing observables")
      for o in observables:
        reset_ccy = o.reset_currency()
        if ccys.count(reset_ccy) == 0:
          ccys.append(reset_ccy)
      if ccys.count(pay_ccy) == 0:
        ccys.append(pay_ccy)
  if len(ccys) != 1:
    raise RuntimeError ("expected one currency")
  return ccys[0]

def enforce_no_exercise_stubs(trd):
  accrual_start_dates = []
  for l in trd.legs():
    for f in l.flows():
      accrual_start_dates.append(f.accrual_start_date())

  if trd.has_exercise_schedule():
    exercises = trd.exercise_schedule()
    for exercise in exercises:
      notification_date = exercise.notification_date()        
      if accrual_start_dates.count(notification_date) == 0:
        raise RuntimeError ("exercise stub encountered")
  
def is_last_flow(lg, flw):
  flws = lg.flows()
  return flw.pay_date() == flws[-1].pay_date()  

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()

