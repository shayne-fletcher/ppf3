class exercise:
  '''
  >>> from ppf.date_time import *
  >>> notification_date = date(2008, Jan, 7)
  >>> exercise_date = date(2008, Jan, 7)
  >>> ex = exercise(notification_date, exercise_date)
  >>> print ex
  2008-Jan-07, 2008-Jan-07, 
  '''
  def __init__(self, notification_date, exercise_date, fee = None, fee_ccy = None):
    self.__notification_date = notification_date
    self.__exercise_date = exercise_date
    self.__fee = fee
    self.__fee_ccy = fee_ccy
    if fee != None and fee_ccy == None:
      raise RuntimeError ("non-zero fee with no currency")

  def notification_date(self): return self.__notification_date
  def exercise_date(self): return self.__exercise_date
  def fee(self): return self.__fee
  def fee_currency(self): return self.__fee_ccy

  def __str__(self):
    s = "%s, " % self.__notification_date
    s += "%s, " % self.__exercise_date
    if self.__fee != None:
      s += "%f, " %  self.__fee
      s += "%s, " % self.__fee_ccy
    return s

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()
