from .observable import *
from .fixing import *

class fixed_coupon(observable):
  def __init__(self
             , attributes
             , flow_id
             , reset_ccy
             , reset_date
             , coupon_rate):
    observable.__init__(self
                      , attributes 
                      , flow_id
                      , 0
                      , reset_ccy
                      , reset_date
                      , reset_date
                      , fixing(True, coupon_rate)
                      , None)
    '''
    >>> from ppf.date_time import *
    >>> t = date(2008, Jan, 7) 
    >>> cpn = fixed_coupon(None, 0, "eur", t, 0.05)
    >>> print cpn.coupon_rate()
    0.05
    '''

  def coupon_rate(self):
    return self.fix().value()

  def __str__(self):
      s = "\"%f\", " % \
        self.flow_id()
      s += "\"%f\", " % \
        self.reset_id()
      s += "\"%s\", " % \
        self.reset_currency()
      s += "\"%f\", " % \
        self.coupon_rate()
  
      return s
    

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
   _test()
