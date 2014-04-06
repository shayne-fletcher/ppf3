import ppf.date_time
from .fixed_coupon import *
from .libor_rate import *
from .swap_rate import *

def generate_fixed_coupon_observables(
   start
 , end
 , roll_period = 6
 , roll_duration = ppf.date_time.months
 , reset_currency = "USD"
 , coupon_holiday_centres = None
 , coupon_shift_method = ppf.date_time.shift_convention.modified_following
 , coupon_rate = 0.05
 , *arguments
 , **keywords):
  '''Generate a sequence of fixed coupons.
  
  >>> from ppf.date_time import *
  >>> observables = generate_fixed_coupon_observables(
  ...     start  = date(2007, Jun, 29)
  ...   , end  = date(2017, Jun, 29)
  ...   , roll_period = 6
  ...   , coupon_shift_method = shift_convention.modified_following
  ...   , coupon_rate = 0.045)
  >>> for obs_per_flow in observables:
  ...  for obs in obs_per_flow:
  ...   print obs
  "0.000000", "0.000000", "USD", "0.045000", 
  "1.000000", "0.000000", "USD", "0.045000", 
  "2.000000", "0.000000", "USD", "0.045000", 
  "3.000000", "0.000000", "USD", "0.045000", 
  "4.000000", "0.000000", "USD", "0.045000", 
  "5.000000", "0.000000", "USD", "0.045000", 
  "6.000000", "0.000000", "USD", "0.045000", 
  "7.000000", "0.000000", "USD", "0.045000", 
  "8.000000", "0.000000", "USD", "0.045000", 
  "9.000000", "0.000000", "USD", "0.045000", 
  "10.000000", "0.000000", "USD", "0.045000", 
  "11.000000", "0.000000", "USD", "0.045000", 
  "12.000000", "0.000000", "USD", "0.045000", 
  "13.000000", "0.000000", "USD", "0.045000", 
  "14.000000", "0.000000", "USD", "0.045000", 
  "15.000000", "0.000000", "USD", "0.045000", 
  "16.000000", "0.000000", "USD", "0.045000", 
  "17.000000", "0.000000", "USD", "0.045000", 
  "18.000000", "0.000000", "USD", "0.045000", 
  "19.000000", "0.000000", "USD", "0.045000", 
  '''

  from ppf.date_time import days
  shift = ppf.date_time.shift

  flow_id = 0
  day = 0
  all_observables = []
  while day < end:
    roll_start = start + roll_duration(flow_id*roll_period)
    roll_end = start + roll_duration((flow_id+1)*roll_period)
    reset_id = 0
    observables = []
    reset_date = shift(roll_start, coupon_shift_method, coupon_holiday_centres)
    observables.append(fixed_coupon(None, flow_id, reset_currency, reset_date, coupon_rate) )
    day = roll_end
    all_observables.append(observables)
    flow_id += 1
  
  return all_observables 

def generate_libor_observables(
   start
 , end
 , roll_period = 6
 , roll_duration = ppf.date_time.months
 , reset_period = 6
 , reset_duration = ppf.date_time.months
 , tenor_period = 6
 , tenor_duration = ppf.date_time.months
 , reset_currency = "USD"
 , reset_basis = ppf.date_time.basis_act_360
 , reset_holiday_centres = None
 , reset_shift_method = ppf.date_time.shift_convention.modified_following
 , reset_lag = 0
 , *arguments
 , **keywords):
  '''Generate a sequence of libor rates.
  
  >>> from ppf.date_time import *
  >>> observables = generate_libor_observables(
  ...     start  = date(2007, Jun, 29)
  ...   , end  = date(2012, Jun, 29)
  ...   , roll_period = 6
  ...   , roll_duration = ppf.date_time.months
  ...   , reset_period = 3
  ...   , reset_duration = ppf.date_time.months
  ...   , tenor_period = 3
  ...   , tenor_duration = ppf.date_time.months
  ...   , reset_currency = "JPY"
  ...   , reset_basis = basis_act_360
  ...   , reset_shift_method = shift_convention.modified_following)
  >>> for obs_per_flow in observables:
  ...  for obs in obs_per_flow:
  ...   print obs
  0, 0, JPY, [2007-Jun-29, 2007-Sep-28], basis_act_360, 
  0, 1, JPY, [2007-Sep-28, 2007-Dec-31], basis_act_360, 
  1, 0, JPY, [2007-Dec-31, 2008-Mar-31], basis_act_360, 
  1, 1, JPY, [2008-Mar-31, 2008-Jun-30], basis_act_360, 
  2, 0, JPY, [2008-Jun-30, 2008-Sep-29], basis_act_360, 
  2, 1, JPY, [2008-Sep-29, 2008-Dec-29], basis_act_360, 
  3, 0, JPY, [2008-Dec-29, 2009-Mar-30], basis_act_360, 
  3, 1, JPY, [2009-Mar-30, 2009-Jun-29], basis_act_360, 
  4, 0, JPY, [2009-Jun-29, 2009-Sep-29], basis_act_360, 
  4, 1, JPY, [2009-Sep-29, 2009-Dec-29], basis_act_360, 
  5, 0, JPY, [2009-Dec-29, 2010-Mar-29], basis_act_360, 
  5, 1, JPY, [2010-Mar-29, 2010-Jun-29], basis_act_360, 
  6, 0, JPY, [2010-Jun-29, 2010-Sep-29], basis_act_360, 
  6, 1, JPY, [2010-Sep-29, 2010-Dec-29], basis_act_360, 
  7, 0, JPY, [2010-Dec-29, 2011-Mar-29], basis_act_360, 
  7, 1, JPY, [2011-Mar-29, 2011-Jun-29], basis_act_360, 
  8, 0, JPY, [2011-Jun-29, 2011-Sep-29], basis_act_360, 
  8, 1, JPY, [2011-Sep-29, 2011-Dec-29], basis_act_360, 
  9, 0, JPY, [2011-Dec-29, 2012-Mar-29], basis_act_360, 
  9, 1, JPY, [2012-Mar-29, 2012-Jun-29], basis_act_360, 
 '''
  from ppf.date_time import days
  shift = ppf.date_time.shift

  if reset_lag > 0:
    raise RuntimeError ("index lag expected less or equal to zero")

  day, flow_id, all_observables = 0, 0, []
  while day < end:
      roll_start = start + roll_duration(flow_id*roll_period)
      roll_end = start + roll_duration((flow_id+1)*roll_period)
      reset_id = 0
      proj_roll = roll_start
      observables = []
      while proj_roll < roll_end:
           proj_start = shift(
                    proj_roll
                  , reset_shift_method, reset_holiday_centres)
           proj_end = shift(
                    proj_roll+tenor_duration(tenor_period)
                  , reset_shift_method, reset_holiday_centres)
           reset_date = shift(
                    proj_start+days(reset_lag)
                  , reset_shift_method, reset_holiday_centres)
           observables.append( 
                     libor_rate(None, flow_id,  reset_id, reset_date
                              , reset_currency, proj_start, proj_end
                              , reset_basis, fixing(False)))
           reset_id += 1
           proj_roll = roll_start+reset_duration(reset_id*reset_period) 
      day = roll_end
      all_observables.append(observables)
      flow_id += 1

  return all_observables

def generate_swap_observables(
   start
 , end
 , attributes
 , spread = 0
 , roll_period = 6
 , roll_duration = ppf.date_time.months
 , tenor_period = 10
 , tenor_duration = ppf.date_time.years
 , reset_currency = "USD"
 , reset_basis = ppf.date_time.basis_act_360
 , reset_holiday_centres = None
 , reset_shift_method = ppf.date_time.shift_convention.modified_following
 , reset_lag = 0
 , *arguments
 , **keywords):
  '''Generate a sequence of swap rates.
  
    >>> from ppf.date_time import *
    >>> props = {}
    >>> props["fixed-pay-period"] = 1
    >>> props["fixed-pay-period-duration"] = years
    >>> props["fixed-pay-basis"] = basis_act_360
    >>> props["fixed-pay-holiday-centers"] = None
    >>> props["fixed-shift-convention"] = modified_following
    >>> props["float-pay-period"] = 6
    >>> props["float-pay-period-duration"] = months
    >>> props["float-pay-basis"] = basis_act_365
    >>> props["float-pay-holiday-centers"] = None
    >>> props["float-shift-convention"] = modified_following
    >>> props["index-basis"] = basis_act_365
    >>> props["index-holiday-centers"] = None
    >>> props["index-shift-convention"] = modified_following
    >>> observables = generate_swap_observables(
    ...     start  = date(2007, Jun, 29)
    ...   , end  = date(2017, Jun, 29)
    ...   , attributes = props
    ...   , roll_period = 1
    ...   , roll_duration = years
    ...   , tenor_period = 10
    ...   , tenor_duration = years)
    >>> for o in observables: print o
    0, 0, USD, [2007-Jun-29, 2017-Jun-29], 
    1, 0, USD, [2008-Jun-30, 2018-Jun-29], 
    2, 0, USD, [2009-Jun-29, 2019-Jun-28], 
    3, 0, USD, [2010-Jun-29, 2020-Jun-29], 
    4, 0, USD, [2011-Jun-29, 2021-Jun-29], 
    5, 0, USD, [2012-Jun-29, 2022-Jun-29], 
    6, 0, USD, [2013-Jun-28, 2023-Jun-29], 
    7, 0, USD, [2014-Jun-30, 2024-Jun-28], 
    8, 0, USD, [2015-Jun-29, 2025-Jun-30], 
    9, 0, USD, [2016-Jun-29, 2026-Jun-29], 
  '''
  from ppf.date_time import days
  shift = ppf.date_time.shift

  if reset_lag > 0:
    raise RuntimeError ("index lag expected less or equal to zero")

  day, flow_id, all_observables = 0, 0, []
  while day < end:
      roll_start = start + roll_duration(flow_id*roll_period)
      roll_end = start + roll_duration((flow_id+1)*roll_period)
      reset_id = 0
      proj_roll = roll_start
      proj_start = \
        shift(
            proj_roll
          , reset_shift_method
          , reset_holiday_centres
          )
      proj_end = \
        shift(
            proj_roll+tenor_duration(tenor_period)
          , reset_shift_method, reset_holiday_centres
          )
      reset_date = \
        shift(
            proj_start+days(reset_lag)
          , reset_shift_method, reset_holiday_centres
          )
      all_observables.append(
        swap_rate(
            attributes
          , flow_id
          , reset_id
          , reset_date
          , reset_currency
          , proj_start
          , proj_end
          , fixing(False)
          , spread) )
      flow_id += 1; reset_id += 1; day = roll_end

  return all_observables
  
def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()
