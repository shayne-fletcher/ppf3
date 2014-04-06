class trade(object):
  '''
    >>> from ppf.date_time import *
    >>> from pay_receive import *
    >>> from generate_flows import *
    >>> from generate_exercise_table import *
    >>> from exercise_type import *
    >>> from leg import *
    >>> #semi-annual flows
    >>> flows = generate_flows(
    ...   start  = date(2007, Jun, 29)
    ...   , end  = date(2017, Jun, 29)
    ...   , duration = ppf.date_time.months
    ...   , period = 6
    ...   , shift_method = shift_convention.modified_following
    ...   , basis = "ACT/360")
    >>> pay_leg = leg(flows, PAY)
    >>> receive_leg = leg(flows, RECEIVE)
    >>> #1y nc
    >>> ex_sched = generate_exercise_table(
    ...   start = date(2008, Jun, 29)
    ... , end  = date(2016, Jun, 29)
    ... , period = 1
    ... , duration = ppf.date_time.years
    ... , shift_method = shift_convention.modified_following)
    >>> structure = trade([pay_leg, receive_leg], [ex_sched, exercise_type.callable])
    >>> print ("callable", "cancellable")[structure.exercise_type() == -1]
    callable
  '''

  def __init__(self, legs, exercise_info=None):
    self.__legs = legs
    self.__exercise_info = exercise_info

  def legs(self):
    return self.__legs

  def exercise_type(self):
    if not self.__exercise_info:
      raise RuntimeError ("missing exercise information")
    return self.__exercise_info[1]

  def exercise_schedule(self):
    if not self.__exercise_info:
      raise RuntimeError ("missing exercise information")
    return self.__exercise_info[0]

  def has_exercise_schedule(self):
    return self.__exercise_info != None
    
def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
