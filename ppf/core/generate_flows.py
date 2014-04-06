import ppf.date_time
from flow import *

def generate_flows(
   start
 , end
 , period = 6
 , duration = ppf.date_time.months
 , notional = 10000000
 , accrual_basis = ppf.date_time.basis_act_360
 , pay_currency = "USD"
 , pay_shift_method  = ppf.date_time.shift_convention.modified_following
 , pay_holiday_centers = None
 , accrual_shift_method  = ppf.date_time.shift_convention.modified_following
 , accrual_holiday_centers = None
 , observables = None
 , *arguments
 , **keywords):
  '''
    >>> from ppf.date_time import *
    >>> flows = generate_flows(
    ...     start  = date(2007, Jun, 29)
    ...   , end  = date(2017, Jun, 29)
    ...   , period = 6
    ...   , duration = ppf.date_time.months
    ...   , notional = 1000000
    ...   , accrual_basis = basis_30360
    ...   , pay_currency = "JPY"
    ...   , pay_shift_method = shift_convention.modified_following)
    >>> for f in flows:
    ...  print f
    1000000.000000, JPY, [2007-Jun-29, 2007-Dec-31], basis_30360, 2007-Dec-31, 
    1000000.000000, JPY, [2007-Dec-31, 2008-Jun-30], basis_30360, 2008-Jun-30, 
    1000000.000000, JPY, [2008-Jun-30, 2008-Dec-29], basis_30360, 2008-Dec-29, 
    1000000.000000, JPY, [2008-Dec-29, 2009-Jun-29], basis_30360, 2009-Jun-29, 
    1000000.000000, JPY, [2009-Jun-29, 2009-Dec-29], basis_30360, 2009-Dec-29, 
    1000000.000000, JPY, [2009-Dec-29, 2010-Jun-29], basis_30360, 2010-Jun-29, 
    1000000.000000, JPY, [2010-Jun-29, 2010-Dec-29], basis_30360, 2010-Dec-29, 
    1000000.000000, JPY, [2010-Dec-29, 2011-Jun-29], basis_30360, 2011-Jun-29, 
    1000000.000000, JPY, [2011-Jun-29, 2011-Dec-29], basis_30360, 2011-Dec-29, 
    1000000.000000, JPY, [2011-Dec-29, 2012-Jun-29], basis_30360, 2012-Jun-29, 
    1000000.000000, JPY, [2012-Jun-29, 2012-Dec-31], basis_30360, 2012-Dec-31, 
    1000000.000000, JPY, [2012-Dec-31, 2013-Jun-28], basis_30360, 2013-Jun-28, 
    1000000.000000, JPY, [2013-Jun-28, 2013-Dec-30], basis_30360, 2013-Dec-30, 
    1000000.000000, JPY, [2013-Dec-30, 2014-Jun-30], basis_30360, 2014-Jun-30, 
    1000000.000000, JPY, [2014-Jun-30, 2014-Dec-29], basis_30360, 2014-Dec-29, 
    1000000.000000, JPY, [2014-Dec-29, 2015-Jun-29], basis_30360, 2015-Jun-29, 
    1000000.000000, JPY, [2015-Jun-29, 2015-Dec-29], basis_30360, 2015-Dec-29, 
    1000000.000000, JPY, [2015-Dec-29, 2016-Jun-29], basis_30360, 2016-Jun-29, 
    1000000.000000, JPY, [2016-Jun-29, 2016-Dec-29], basis_30360, 2016-Dec-29, 
    1000000.000000, JPY, [2016-Dec-29, 2017-Jun-29], basis_30360, 2017-Jun-29, 
  '''

  i, day  = 0, start
  flows = []
  shift = ppf.date_time.shift
  while day < end:
      roll_start = start + duration(i*period)
      roll_end = start + duration((i + 1)*period) 
      accrual_start = shift(
              roll_start
            , accrual_shift_method, accrual_holiday_centers)
      accrual_end = shift(
              roll_end
            , accrual_shift_method, accrual_holiday_centers)
      pay = shift(
              roll_end
            , pay_shift_method, pay_holiday_centers)
      flows.append(
        flow(notional
           , pay_currency
           , accrual_start
           , accrual_end
           , accrual_basis
           , pay)
        )
      day = roll_end
      i += 1
      
  if observables <> None:
    if len(observables) <> len(flows):
      raise RuntimeError, "too few or too many observables"
    for i in range(len(flows)):
      f = flows[i]
      obs = observables[i]
      f.set_observables(obs)
  return flows

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
