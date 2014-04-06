import ppf.date_time
from .adjuvant_table import *

def generate_adjuvant_table(
   keys
 , tenors
 , values
 , start_date
 , roll_period = 6
 , roll_duration = ppf.date_time.months
 , holiday_centres = None
 , shift_method = ppf.date_time.shift_convention.modified_following
 , *arguments
 , **keywords):
  '''
  >>> from ppf.date_time import *
  >>> from numpy import *
  >>> adjuvants = generate_adjuvant_table(
  ...     keys = ["spread","coupon"]
  ...   , tenors = [12,24,36]
  ...   , values = array([[0.005, 0.006, 0.007], [0.05, 0.06, 0.07]])
  ...   , start_date  = date(2008, May, 1)
  ...   , roll_period = 6
  ...   , shift_method = shift_convention.modified_following)
  >>> print adjuvants
  {'coupon': {2455138: 0.06, 2455684: 0.07, 2454953: 0.05, 2455502: 0.07, 2454774: 0.05, 2455320: 0.06}, 'spread': {2455138: 0.006, 2455684: 0.007, 2454953: 0.005, 2455502: 0.007, 2454774: 0.005, 2455320: 0.006}}

  '''
  if len(values.shape) != 2:
    raise RuntimeError ("expected 2d array of values")
  if len(keys) != values.shape[0] or len(tenors) != values.shape[1]:
    raise RuntimeError ("incorrect size of values array")

  from ppf.date_time import days
  shift = ppf.date_time.shift

  day = 0
  dates = []
  indices = []
  cnt = 0
  start = start_date
  for tenor in tenors:
    end = start_date+roll_duration(tenor)
    if end < day:
      raise RuntimeError ("tenors are not monotonically increasing")
    i = 0    
    while day < end:
      roll_start = start+roll_duration(i*roll_period)
      roll_end = start+roll_duration((i+1)*roll_period)
      pay = shift(roll_end, shift_method, holiday_centres)
      day = pay
      dates.append(day)
      indices.append(cnt)
      i += 1
    cnt += 1
    start = end
    
  import numpy
  all_values = numpy.zeros((len(keys), len(dates)))
  for i in range(len(keys)):
    for j in range(len(dates)):
      idx = indices[j]
      all_values[i][j] = values[i][idx]
  return adjuvant_table(keys, dates, all_values)

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
