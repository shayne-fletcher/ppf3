from ppf_date_time import  \
     weekdays              \
   , months_of_year        \
   , nth_kday_of_month     \
   , year_based_generator  \

class nth_imm_of_year(year_based_generator):
  '''Calculate the nth IMM date for a given year

    >>> imm = nth_imm_of_year
    >>> imm_dates = []
    >>> imm_dates.append(imm(imm.first).get_date(2005))
    >>> imm_dates.append(imm(imm.second).get_date(2005))
    >>> imm_dates.append(imm(imm.third).get_date(2005))
    >>> imm_dates.append(imm(imm.fourth).get_date(2005))
    >>> for t in imm_dates:
    ...   print t
    2005-Mar-16
    2005-Jun-15
    2005-Sep-21
    2005-Dec-21

  '''
  first = months_of_year.Mar
  second = months_of_year.Jun
  third = months_of_year.Sep
  fourth = months_of_year.Dec

  def __init__(self, which):
    year_based_generator.__init__(self)
    self._month = which

  def get_date(self, year):
    return nth_kday_of_month(
          nth_kday_of_month.third
        , weekdays.Wednesday
        , self._month).get_date(year)

  def to_string(self):
    pass

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()
    
