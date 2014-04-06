class leg(object):
  '''
    >>> from ppf.date_time import *
    >>> from pay_receive import *
    >>> from generate_flows import *
    >>> flows = generate_flows(
    ...   start  = date(2007, Jun, 29)
    ...   , end  = date(2017, Jun, 29)
    ...   , resolution = date_resolutions.months
    ...   , period = 6
    ...   , shift_method = shift_convention.modified_following
    ...   , basis = "ACT/360")
    >>>
    >>> pay_leg = leg(flows, PAY)
    >>>
    >>> for flow in pay_leg.flows():
    ...  print flow
    10000000.000000, USD, [2007-Jun-29, 2007-Dec-31], basis_act_360, 2007-Dec-31, 
    10000000.000000, USD, [2007-Dec-31, 2008-Jun-30], basis_act_360, 2008-Jun-30, 
    10000000.000000, USD, [2008-Jun-30, 2008-Dec-29], basis_act_360, 2008-Dec-29, 
    10000000.000000, USD, [2008-Dec-29, 2009-Jun-29], basis_act_360, 2009-Jun-29, 
    10000000.000000, USD, [2009-Jun-29, 2009-Dec-29], basis_act_360, 2009-Dec-29, 
    10000000.000000, USD, [2009-Dec-29, 2010-Jun-29], basis_act_360, 2010-Jun-29, 
    10000000.000000, USD, [2010-Jun-29, 2010-Dec-29], basis_act_360, 2010-Dec-29, 
    10000000.000000, USD, [2010-Dec-29, 2011-Jun-29], basis_act_360, 2011-Jun-29, 
    10000000.000000, USD, [2011-Jun-29, 2011-Dec-29], basis_act_360, 2011-Dec-29, 
    10000000.000000, USD, [2011-Dec-29, 2012-Jun-29], basis_act_360, 2012-Jun-29, 
    10000000.000000, USD, [2012-Jun-29, 2012-Dec-31], basis_act_360, 2012-Dec-31, 
    10000000.000000, USD, [2012-Dec-31, 2013-Jun-28], basis_act_360, 2013-Jun-28, 
    10000000.000000, USD, [2013-Jun-28, 2013-Dec-30], basis_act_360, 2013-Dec-30, 
    10000000.000000, USD, [2013-Dec-30, 2014-Jun-30], basis_act_360, 2014-Jun-30, 
    10000000.000000, USD, [2014-Jun-30, 2014-Dec-29], basis_act_360, 2014-Dec-29, 
    10000000.000000, USD, [2014-Dec-29, 2015-Jun-29], basis_act_360, 2015-Jun-29, 
    10000000.000000, USD, [2015-Jun-29, 2015-Dec-29], basis_act_360, 2015-Dec-29, 
    10000000.000000, USD, [2015-Dec-29, 2016-Jun-29], basis_act_360, 2016-Jun-29, 
    10000000.000000, USD, [2016-Jun-29, 2016-Dec-29], basis_act_360, 2016-Dec-29, 
    10000000.000000, USD, [2016-Dec-29, 2017-Jun-29], basis_act_360, 2017-Jun-29, 
  '''
  def __init__(self, flows, pay_or_receive, adjuvant_table = None, payoff = None):
    self.__flows = flows
    self.__pay_or_receive = pay_or_receive
    self.__adjuvant_table = adjuvant_table
    self.__payoff = payoff

  def flows(self):
    return self.__flows

  def pay_receive(self):
    return self.__pay_or_receive

  def has_adjuvant_table(self):
    return self.__adjuvant_table != None

  def has_payoff(self):
    return self.__payoff != None

  def adjuvant_table(self):
    if self.__adjuvant_table == None:
      raise RumtimeError ("Null adjuvant table")
    return self.__adjuvant_table

  def payoff(self):
    if self.__payoff == None:
      raise RumtimeError ("Null payoff")
    return self.__payoff

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()

