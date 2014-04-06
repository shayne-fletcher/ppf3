class observable(object):
  def __init__(self
             , attributes
             , flow_id
             , reset_id
             , reset_ccy
             , reset_date
             , last_important_date
             , fix
             , spread):
    '''
    >>> from ppf.date_time import *
    >>> from observable import *
    >>> x = observable(None, 1, 1, "eur", date(2008, Jan, 6), date(2008, Jan, 6), None, None)
    >>> print x.reset_date()
    2008-Jan-06

    '''
    self.__attributes = attributes
    self.__flow_id = flow_id
    self.__reset_id = reset_id
    self.__reset_ccy = reset_ccy
    self.__reset_date = reset_date
    self.__last_important_date = last_important_date
    self.__fix = fix
    self.__spread = spread

  def flow_id(self): return self.__flow_id
  def reset_id(self): return self.__reset_id
  def reset_currency(self): return self.__reset_ccy
  def reset_date(self): return self.__reset_date
  def last_important_date(self): return self.__last_important_date
  def spread(self): return self.__spread
  def fix(self) : return self.__fix
  def attributes(self) : return self.__attributes

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()

