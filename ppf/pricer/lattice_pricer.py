import string
from ppf.core import trade_utils
from ppf.core.trade import *
from ppf.core.event import *
from ppf.core.timeline import *
from ppf.core.controller import *
from ppf.market import *
from ppf.model import *
from ppf.core.exercise_type import *

class lattice_pricer(object):
  def __init__(self, trade, model, env, symbol_table_listener = None):
    self.__trade = trade
    self.__model = model
    self.__env = env
    self.__symbol_table_listener = symbol_table_listener
    # check no stubs
    trade_utils.enforce_no_exercise_stubs(trade)
    # create timeline
    self.__timeline = timeline(trade, env.pricing_date())   

  def __symbol_listener_(self, t, symbol, value):
    if self.__symbol_table_listener:
      self.__symbol_table_listener(t, symbol, value, self.__model, self.__env)

  def __call__(self):
    '''
    >>> from ppf.date_time import *
    >>> import math
    >>> from ppf.math.interpolation import loglinear
    >>> times = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0]
    >>> factors = [math.exp(-0.05*t) for t in times]
    >>> import ppf.market
    >>> c = ppf.market.curve(times, factors, loglinear)
    >>> from numpy import zeros
    >>> expiries = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0]
    >>> tenors = [0, 90]
    >>> values = zeros((14, 2))
    >>> for i in range(14): values[i, 0] = 0.01
    >>> for i in range(14): values[i, 1] = 0.01
    >>> surf = ppf.market.surface(expiries, tenors, values)
    >>> env = ppf.market.environment(date(2007, Mar, 29))
    >>> key = "zc.disc.usd"
    >>> env.add_curve(key, c)
    >>> key = "ve.term.usd.hw"
    >>> env.add_surface(key, surf)
    >>> key = "cv.mr.usd.hw"
    >>> env.add_constant(key, 0.01)
    >>> from ppf.core.pay_receive import *
    >>> from ppf.core.generate_flows import *
    >>> from ppf.core.generate_observables import *
    >>> from ppf.core.generate_exercise_table import *
    >>> from ppf.core.exercise_type import *
    >>> from ppf.core.leg import *
    >>> from ppf.core.trade import *
    >>> libor_observables = generate_libor_observables(
    ...     start  = date(2007, Jun, 29)
    ...   , end  = date(2010, Jun, 29)
    ...   , roll_period = 6
    ...   , roll_duration = ppf.date_time.months
    ...   , reset_period = 6
    ...   , reset_duration = ppf.date_time.months
    ...   , reset_currency = "USD"
    ...   , reset_basis = basis_act_360
    ...   , reset_shift_method = shift_convention.modified_following)
    >>> coupon_observables = generate_fixed_coupon_observables(
    ...     start  = date(2007, Jun, 29)
    ...   , end  = date(2010, Jun, 29)
    ...   , roll_period = 6
    ...   , reset_currency = "USD"
    ...   , coupon_shift_method = shift_convention.modified_following
    ...   , coupon_rate = 0.045)
    >>> #semi-annual flows
    >>> pay_flows = generate_flows(
    ...   start  = date(2007, Jun, 29)
    ...   , end  = date(2010, Jun, 29)
    ...   , duration = ppf.date_time.months
    ...   , period = 6
    ...   , notional = 0
    ...   , pay_shift_method = shift_convention.modified_following
    ...   , pay_currency = "USD"
    ...   , basis = "30/360"
    ...   , observables = coupon_observables)
    >>> from ppf.core.generate_adjuvant_table import *
    >>> from numpy import array
    >>> rcv_flows = generate_flows(
    ...   start  = date(2007, Jun, 29)
    ...   , end  = date(2010, Jun, 29)
    ...   , duration = ppf.date_time.months
    ...   , period = 6
    ...   , pay_shift_method = shift_convention.modified_following
    ...   , pay_currency = "USD"
    ...   , basis = "A/360"
    ...   , observables = libor_observables)
    >>> rcv_adjuvant_table = generate_adjuvant_table(
    ...   keys = ["spread0"]
    ...   , tenors = [48]
    ...   , values = array([[0.0]])
    ...   , shift_method = shift_convention.modified_following
    ...   , start_date = date(2007, Jun, 29))
    >>> from ppf.pricer import *
    >>> pay_leg = leg(pay_flows, PAY, None, payoffs.fixed_leg_payoff())
    >>> receive_leg = leg(rcv_flows, RECEIVE, rcv_adjuvant_table, payoffs.float_leg_payoff())
    >>> #1y nc
    >>> ex_sched = generate_exercise_table(
    ...   start = date(2007, Jun, 29)
    ... , end  = date(2009, Jun, 29)
    ... , period = 1
    ... , duration = ppf.date_time.years
    ... , shift_method = shift_convention.modified_following)
    >>> structure = trade((pay_leg, receive_leg))#, (ex_sched, exercise_type.callable))
    >>> from ppf.model import *
    >>> factory = hull_white_lattice_model_factory()
    >>> model = factory(structure, env)
    >>> pricer = lattice_pricer(structure, model, env)
    >>> print pricer()
    1376834.46742
    '''
    # create controller
    ctr = controller(self.__trade, self.__model, self.__env)
    times = self.__timeline.times()
    from_ = self.__env.relative_date(times[-1])/365.0
    # initialise symbols
    ctr.insert_symbol("underlying", from_)
    ctr.insert_symbol("berm", from_)
    cnt = 0
    for l in self.__trade.legs():
      symbol = "leg"+str(cnt)
      ctr.insert_symbol(symbol, from_)      
      cnt += 1
    # reverse iterate through the timeline
    for i in range(len(times)-1,-1,-1):
       time = times[i]
       to_ = 0
       if i <> 0:
         to_ = self.__env.relative_date(times[i-1])/365.0
       events = self.__timeline.events(time)
       for event in events:
         # set event on controller
         ctr.set_event(event)
         # evaluate
         if is_pay_event(event):
           #print 'evaluating leg ', event.leg_id(), ' at ', from_          
           # evaluate payoff
           cpn = ctr(from_)
           # rollback symbol
           symbol = "leg"+str(event.leg_id())
           leg_pv = ctr.retrieve_symbol(symbol) 
           leg_pv += cpn        
           self.__symbol_listener_(from_, symbol, leg_pv)
           ctr.update_symbol(symbol, leg_pv, from_)   
         else:
           #print 'evaluating  berm at ', from_          
           # evaluate underlying             
           underlying = ctr.retrieve_symbol("underlying")
           underlying *= 0 # not pretty
           cnt = 0
           for l in self.__trade.legs():
             underlying += ctr.retrieve_symbol("leg"+str(cnt))         
             cnt += 1
           self.__symbol_listener_(from_, "underlying", self.__trade.exercise_type()*underlying)
           # rollback berm
           berm = ctr.retrieve_symbol("berm")
           self.__symbol_listener_(from_, "berm", berm)
           berm = ctr.rollback_max(from_, to_, berm, self.__trade.exercise_type()*underlying)
           # rollback underlying
           underlying = ctr.rollback(from_, to_, underlying)
           # update symbols
           ctr.update_symbol("underlying", underlying, to_)
           ctr.update_symbol("berm", berm, to_)
       # rollback any symbols in symbol table not already rolled back
       symbols = ctr.retrieve_symbols_to_rollback(to_)
       for symbol in symbols:
         from_ = ctr.retrieve_symbol_update_time(symbol)
         value = ctr.retrieve_symbol(symbol)
         value = ctr.rollback(from_, to_, value)
         ctr.update_symbol(symbol, value, to_)
       from_ = to_
    # calculate pv
    underlying = ctr.retrieve_symbol("underlying")
    underlying *= 0
    cnt = 0
    for l in self.__trade.legs():
      underlying += ctr.retrieve_symbol("leg"+str(cnt))         
      cnt += 1
    ctr.update_symbol("underlying", underlying, to_)
    pv = 0
    if self.__trade.has_exercise_schedule():
      if self.__trade.exercise_type() == exercise_type.callable:
        pv = ctr.retrieve_symbol("berm").mean()
      else:
        pv = ctr.retrieve_symbol("underlying").mean()+ctr.retrieve_symbol("berm").mean()
    else:
      pv = ctr.retrieve_symbol("underlying").mean()
    return pv

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()

  
