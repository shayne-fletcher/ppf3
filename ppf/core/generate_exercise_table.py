import ppf.date_time
from .exercise import *

def generate_exercise_table(
   start
 , end
 , period = 6
 , duration = ppf.date_time.months
 , shift_method  = ppf.date_time.shift_convention.modified_following
 , basis = ppf.date_time.basis_act_360
 , holiday_centers = None
 , fee = None 
 , fee_currency = None
 , *arguments
 , **keywords):
  '''
   >>> from ppf.date_time import *
   >>> ex_sched = generate_exercise_table(
   ...   start  = date(2007, Jun, 29)
   ... , end  = date(2017, Jun, 29)
   ... , duration = months
   ... , period = 6
   ... , fee = 1000000
   ... , fee_currency = "EUR"
   ... , shift_method = shift_convention.modified_following)
   >>> for ex in ex_sched: print ex
   2007-Jun-29, 2007-Jun-29, 1000000.000000, EUR, 
   2007-Dec-31, 2007-Dec-31, 1000000.000000, EUR, 
   2008-Jun-30, 2008-Jun-30, 1000000.000000, EUR, 
   2008-Dec-29, 2008-Dec-29, 1000000.000000, EUR, 
   2009-Jun-29, 2009-Jun-29, 1000000.000000, EUR, 
   2009-Dec-29, 2009-Dec-29, 1000000.000000, EUR, 
   2010-Jun-29, 2010-Jun-29, 1000000.000000, EUR, 
   2010-Dec-29, 2010-Dec-29, 1000000.000000, EUR, 
   2011-Jun-29, 2011-Jun-29, 1000000.000000, EUR, 
   2011-Dec-29, 2011-Dec-29, 1000000.000000, EUR, 
   2012-Jun-29, 2012-Jun-29, 1000000.000000, EUR, 
   2012-Dec-31, 2012-Dec-31, 1000000.000000, EUR, 
   2013-Jun-28, 2013-Jun-28, 1000000.000000, EUR, 
   2013-Dec-30, 2013-Dec-30, 1000000.000000, EUR, 
   2014-Jun-30, 2014-Jun-30, 1000000.000000, EUR, 
   2014-Dec-29, 2014-Dec-29, 1000000.000000, EUR, 
   2015-Jun-29, 2015-Jun-29, 1000000.000000, EUR, 
   2015-Dec-29, 2015-Dec-29, 1000000.000000, EUR, 
   2016-Jun-29, 2016-Jun-29, 1000000.000000, EUR, 
   2016-Dec-29, 2016-Dec-29, 1000000.000000, EUR, 
   2017-Jun-29, 2017-Jun-29, 1000000.000000, EUR, 
  '''
  i, day, exercises = 0, 0, []
  shift = ppf.date_time.shift
  while day < end:
    roll_start = start + duration(i*period)
    roll_end = start + duration((i+1)*period)
    exercise_date = shift(
        roll_start
      , shift_method, holiday_centers)
    # assume no notification lag
    exercises.append(
         exercise(exercise_date, exercise_date, fee, fee_currency))  
    day = exercise_date
    i += 1
  return exercises

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()

    
