from ppf_date_time import  \
     weekdays              \
   , months_of_year        \
   , nth_kday_of_month     \
   , year_based_generator
from nth_imm_of_year import *

def first_imm_before(start):
  '''Find the IMM date immediately preceding the given date.

     >>> from ppf_date_time import date
     >>> from ppf_date_time import months_of_year
     >>> Jun = months_of_year.Jun
     >>> print first_imm_before(date(2007, Jun, 27))
     2007-Jun-20

  '''
  imm = nth_imm_of_year
  first_imm_of_year = imm(imm.first).get_date(start.year())
  imm_date = None
  if start <= first_imm_of_year:
    imm_date = imm(imm.fourth).get_date(start.year() - 1)
  else:
    for imm_no in reversed([imm.first, imm.second, imm.third, imm.fourth]):
      imm_date = imm(imm_no).get_date(start.year())
      if imm_date < start:
        break

  return imm_date

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()
