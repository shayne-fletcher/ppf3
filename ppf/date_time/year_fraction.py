from ppf_date_time \
     import date, gregorian_calendar_base
from day_count_basis import *

is_leap_year = gregorian_calendar_base.is_leap_year

def year_fraction(start, until, basis):
  '''Compute accruals

  >>> from ppf_date_time import *
  >>> from day_count_basis import *
  >>> add_months = month_functor
  >>> Nov = months_of_year.Nov
  >>> begin = date(2004, Nov, 21)
  >>> until = begin + add_months(6).get_offset(begin)
  >>> year_fraction(begin, until, day_count_basis.basis_30360)
  0.5
  >>> year_fraction(begin, until, day_count_basis.basis_act_365)
  0.49589041095890413
  >>> year_fraction(begin, until, day_count_basis.basis_act_act)
  0.49285126132195523

  '''
  result = 0
  if basis == day_count_basis.basis_act_360:
    result = (until - start).days()/360.0
  elif basis == day_count_basis.basis_act_365:
    result = (until - start).days()/365.0
  elif basis == day_count_basis.basis_act_act:
    if start.year() != until.year():
      start_of_to_year = date(until.year(), 1, 1)
      end_of_start_year = date(start.year(), 12, 31)
      result = (end_of_start_year - start).days()/ \
          (365.0, 366.0)[is_leap_year(start.year())] \
        +  (int(until.year()) - int(start.year()) - 1) + \
           (until - start_of_to_year).days()/ \
              (365.0, 366.0)[is_leap_year(until.year())]
    else:
      result = (until - start).days()/ \
               (365.0, 366.0)[is_leap_year(util.year())]
  elif basis == day_count_basis.basis_30360:
    d1, d2 = start.day(), until.day()
    if d1 == 31:
        d1 -= 1
    if d2 == 31:
        d2 -= 1
    result = (int(d2) - int(d1)) + \
             30.0*(int(until.month()) - int(start.month())) + \
                      360.0*(int(until.year()) - int(start.year()))
    result = result / 360.0
  else:
    raise RuntimeError ("Unsupported basis")

  return result

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()
