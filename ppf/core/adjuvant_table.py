class adjuvant_table(object):
  def __init__(self, keys, dates, values):
    if len(values.shape) <> 2:
      raise RuntimeError, "expected 2d array of values"
    if len(keys) <> values.shape[0] or len(dates) <> values.shape[1]:
      raise RuntimeError, "incorrect size of values array"
    self.__table = {}
    i = 0
    for key in keys:
      elem = {}
      j = 0
      for dt in dates:        
        elem[dt.julian_day()] = values[i][j]
        j += 1
      self.__table[key] = elem
      i += 1

  def __call__(self, key, dt):
    if self.__table.has_key(key):
       elem = self.__table.get(key)
       if elem.has_key(dt.julian_day()):
         return elem.get(dt.julian_day())
       else:
         raise RuntimeError, "unable to find date in adjuvant table"+" dt = "+str(dt)
    else:
       raise RuntimeError, "unable to find key in adjuvant table"

  def __str__(self):
    '''
    >>> from ppf.date_time import *
    >>> keys = ["spread","coupon"]
    >>> dates = [date(2008, 5, 1), date(2009, 5, 1), date(2010, 5, 1)]
    >>> from numpy import *
    >>> values = zeros((2, 3))
    >>> for i in range(2):
    ...   for j in range(3):
    ...     values[i][j] = (i+1)*0.05+0.001
    >>> table = adjuvant_table(keys, dates, values)
    >>> print table("spread", date(2008, 5, 1))
    0.051
    '''
    return self.__table.__str__()

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
