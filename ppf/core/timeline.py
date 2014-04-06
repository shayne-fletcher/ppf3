from types import *
from trade import *
from leg import *
from flow import *
from exercise import *
from event import *

class timeline(object):
  '''
  >>> from ppf.date_time import *
  >>> from pay_receive import *
  >>> from generate_flows import *
  >>> from generate_observables import *
  >>> from generate_exercise_table import *
  >>> from exercise_type import *
  >>> from leg import *
  >>> from trade import *
  >>> libor_observables = generate_libor_observables(
  ...     start  = date(2007, Jun, 29)
  ...   , end  = date(2009, Jun, 29)
  ...   , roll_period = 6
  ...   , roll_duration = ppf.date_time.months
  ...   , reset_period = 3
  ...   , reset_duration = ppf.date_time.months
  ...   , reset_currency = "JPY"
  ...   , reset_basis = basis_act_360
  ...   , reset_shift_method = shift_convention.modified_following)
  >>> coupon_observables = generate_fixed_coupon_observables(
  ...     start  = date(2007, Jun, 29)
  ...   , end  = date(2009, Jun, 29)
  ...   , roll_period = 6
  ...   , reset_currency = "JPY"
  ...   , coupon_shift_method = shift_convention.modified_following
  ...   , coupon_rate = 0.045)
  >>> #semi-annual flows
  >>> pay_flows = generate_flows(
  ...   start  = date(2007, Jun, 29)
  ...   , end  = date(2009, Jun, 29)
  ...   , duration = ppf.date_time.months
  ...   , period = 6
  ...   , shift_method = shift_convention.modified_following
  ...   , basis = "30/360"
  ...   , observables = coupon_observables)
  >>> rcv_flows = generate_flows(
  ...   start  = date(2007, Jun, 29)
  ...   , end  = date(2009, Jun, 29)
  ...   , duration = ppf.date_time.months
  ...   , period = 6
  ...   , shift_method = shift_convention.modified_following
  ...   , basis = "A/360"
  ...   , observables = libor_observables)
  >>> pay_leg = leg(pay_flows, PAY)
  >>> receive_leg = leg(rcv_flows, RECEIVE)
  >>> #1y nc
  >>> ex_sched = generate_exercise_table(
  ...   start = date(2008, Jun, 29)
  ... , end  = date(2009, Jun, 29)
  ... , period = 1
  ... , duration = ppf.date_time.years
  ... , shift_method = shift_convention.modified_following)
  >>> structure = trade((pay_leg, receive_leg), (ex_sched, exercise_type.callable))
  >>> pricing_date = date(2007, Jan, 29)
  >>> tline = timeline(structure, pricing_date)
  >>> print tline
  events: 
  "2454281", payment [-1, 0, 0, 10000000.000000, USD, [2007-Jun-29, 2007-Dec-31], basis_act_360, 2007-Dec-31, "0.000000", "0.000000", "JPY", "0.045000", ], payment [1, 1, 0, 10000000.000000, USD, [2007-Jun-29, 2007-Dec-31], basis_act_360, 2007-Dec-31, 0, 0, JPY, [2007-Jun-29, 2007-Dec-31], basis_act_360, 0, 1, JPY, [2007-Sep-28, 2008-Mar-31], basis_act_360, ], 
  "2454372", payment [1, 1, 1, 10000000.000000, USD, [2007-Jun-29, 2007-Dec-31], basis_act_360, 2007-Dec-31, 0, 0, JPY, [2007-Jun-29, 2007-Dec-31], basis_act_360, 0, 1, JPY, [2007-Sep-28, 2008-Mar-31], basis_act_360, ], 
  "2454466", payment [-1, 0, 0, 10000000.000000, USD, [2007-Dec-31, 2008-Jun-30], basis_act_360, 2008-Jun-30, "1.000000", "0.000000", "JPY", "0.045000", ], payment [1, 1, 0, 10000000.000000, USD, [2007-Dec-31, 2008-Jun-30], basis_act_360, 2008-Jun-30, 1, 0, JPY, [2007-Dec-31, 2008-Jun-30], basis_act_360, 1, 1, JPY, [2008-Mar-31, 2008-Sep-29], basis_act_360, ], 
  "2454557", payment [1, 1, 1, 10000000.000000, USD, [2007-Dec-31, 2008-Jun-30], basis_act_360, 2008-Jun-30, 1, 0, JPY, [2007-Dec-31, 2008-Jun-30], basis_act_360, 1, 1, JPY, [2008-Mar-31, 2008-Sep-29], basis_act_360, ], 
  "2454648", payment [-1, 0, 0, 10000000.000000, USD, [2008-Jun-30, 2008-Dec-29], basis_act_360, 2008-Dec-29, "2.000000", "0.000000", "JPY", "0.045000", ], payment [1, 1, 0, 10000000.000000, USD, [2008-Jun-30, 2008-Dec-29], basis_act_360, 2008-Dec-29, 2, 0, JPY, [2008-Jun-30, 2008-Dec-29], basis_act_360, 2, 1, JPY, [2008-Sep-29, 2009-Mar-30], basis_act_360, ], exercise [1, 2008-Jun-30, 2008-Jun-30, ], 
  "2454739", payment [1, 1, 1, 10000000.000000, USD, [2008-Jun-30, 2008-Dec-29], basis_act_360, 2008-Dec-29, 2, 0, JPY, [2008-Jun-30, 2008-Dec-29], basis_act_360, 2, 1, JPY, [2008-Sep-29, 2009-Mar-30], basis_act_360, ], 
  "2454830", payment [-1, 0, 0, 10000000.000000, USD, [2008-Dec-29, 2009-Jun-29], basis_act_360, 2009-Jun-29, "3.000000", "0.000000", "JPY", "0.045000", ], payment [1, 1, 0, 10000000.000000, USD, [2008-Dec-29, 2009-Jun-29], basis_act_360, 2009-Jun-29, 3, 0, JPY, [2008-Dec-29, 2009-Jun-29], basis_act_360, 3, 1, JPY, [2009-Mar-30, 2009-Sep-29], basis_act_360, ], 
  "2454921", payment [1, 1, 1, 10000000.000000, USD, [2008-Dec-29, 2009-Jun-29], basis_act_360, 2009-Jun-29, 3, 0, JPY, [2008-Dec-29, 2009-Jun-29], basis_act_360, 3, 1, JPY, [2009-Mar-30, 2009-Sep-29], basis_act_360, ], 
  "2455012", exercise [1, 2009-Jun-29, 2009-Jun-29, ], 
  <BLANKLINE>
  '''

  def __add_event_(self, t, event):
    if not self.__events.has_key(t.julian_day()):
      self.__events[t.julian_day()] = []
    #print 'adding event ', event, ' at time ', t.julian_day()
    self.__events.get(t.julian_day()).append(event)
    #print 'number of events at time ' , t.julian_day(), ' is ', len(self.__events.get(t.julian_day()))

  def __init__(self, trade, pricing_date):
    self.__events = {}

    # add events from legs
    leg_id = 0
    for l in trade.legs():
      pay_rcv = l.pay_receive()
      for f in \
        [f for f in l.flows()
         if f.pay_date() >= pricing_date]:
        observables = f.observables()
        if not observables:
          raise RuntimeError, "Missing observables"
        for o in observables:
          self.__add_event_(
              o.reset_date()
            , pay_event(f, pay_rcv, leg_id, o.reset_id()))
      leg_id += 1

    # add events from exercise schedule
    if trade.has_exercise_schedule():
      ex_type = trade.exercise_type()
      for ex in \
        [ex for ex in trade.exercise_schedule()
         if ex.notification_date() > pricing_date]:
        self.__add_event_(
            ex.notification_date()
          , exercise_event(ex, ex_type))

  def times(self):
    return sorted(self.__events.keys())

  def events(self, t):
    return self.__events[t]

  def __str__(self):
    s = "events: \n"
    times = sorted(self.__events.keys())
    for t in times:
      s += "\"%s\", " % t
      events = self.__events[t]
      for event in events: s += str(event)
      s += '\n'
    return s

  def number_of_exercises(self):
    cnt = 0
    for key in self.__events.keys():
      events = self.__events[key]
      for event in events:
        if is_exercise_event(event):
          cnt += 1
    return cnt

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
 
