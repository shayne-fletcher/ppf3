from ppf_date_time import weekdays

def is_business_day(t, financial_centers=None):
  ''' Test whether the given date is a business day.
      In this version, only weekends are considered
      holidays.
  
      >>> from ppf_date_time import date
      >>> from ppf_date_time import months_of_year
      >>> Jun = months_of_year.Jun
      >>> print is_business_day(date(2007, Jun, 27))
      True
      >>> print is_business_day(date(2007, Jun, 30))
      False

  '''
  Saturday, Sunday = weekdays.Saturday, weekdays.Sunday

  return t.day_of_week().as_number() != Saturday \
       and t.day_of_week().as_number() != Sunday

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()
