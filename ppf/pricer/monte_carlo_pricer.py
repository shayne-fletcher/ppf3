import string
import numpy
from ppf.core import trade_utils
from ppf.core.trade import *
from ppf.core.event import *
from ppf.core.timeline import *
from ppf.core.controller import *
from ppf.market import *
from ppf.model import *
from ppf.core.exercise_type import *
from ppf.math.exercise_regressions import *

# class for managing the exercise indicator function
class exercise_helper(object):
  def __init__(self, num_sims):
    self.__num_sims = num_sims
    self.__last_cfs = numpy.zeros((num_sims))
    self.__indicator = numpy.zeros((num_sims))
    self.__indicator.fill(-1)

  def set_last_cfs(self, cfs):
    self.__last_cfs = cfs.copy() # deep copy

  def update_indicator(self, at, vs, fo):
    regression_value = evaluate_regression(vs, fo)
    for i in range(self.__num_sims):
      if self.__indicator[i] < 0:
        if regression_value[i] > 0:
          self.__indicator[i] = at
        else:
          self.__indicator[i] = -1
 
  def max(self, at, cfs, hv):
    res = numpy.zeros((self.__num_sims))
    for i in range(self.__num_sims):
      value = 0.0
      if self.__indicator[i] > 0 and self.__indicator[i] <= at + 0.01:
        value = cfs[i]-self.__last_cfs[i] # cash flow(s) between exercise dates
      res[i] = hv[i]+value      
    self.__last_cfs = cfs.copy() # deep copy
    return res    

class monte_carlo_pricer(object):
  def __init__(self, trade, model, env, symbol_table_listener = None, regression_model = None):
    self.__trade = trade
    self.__model = model
    self.__env = env
    self.__symbol_table_listener = symbol_table_listener
    self.__regression_model = regression_model
    self.__fitted_fos = None
    self.__exercise_helper = None
    # check no stubs
    trade_utils.enforce_no_exercise_stubs(trade)
    # create timeline
    self.__timeline = timeline(trade, env.pricing_date())   
    # check regression model present if callable
    if self.__trade.has_exercise_schedule() and self.__regression_model == None:
      raise RuntimeError, "exercise schedule present but no 'regression model'"

  def __symbol_listener_(self, t, symbol, value):
    if self.__symbol_table_listener:
      self.__symbol_table_listener(t, symbol, value, self.__model, self.__env)

  def __exercise_boundary_regression(self, symbol_value_pairs_to_add):
    num_expl_vars = self.__regression_model.exercise().num_explanatory_variables()
    num_sims = self.__regression_model.state().num_sims()
    num_exercises = self.__timeline.number_of_exercises()
    # create controller
    ctr = controller(self.__trade, self.__regression_model, self.__env, 1.0)
    times = self.__timeline.times()
    from_ = 0.0
    # initialise symbols
    ctr.insert_symbol("underlying", from_)
    # add extra symbols
    if symbol_value_pairs_to_add:
      for symbol_value_pair in symbol_value_pairs_to_add:
        symbol, value = symbol_value_pair
        ctr.insert_symbol(symbol, value)
    cnt = 0
    for l in self.__trade.legs():
      symbol = "leg"+str(cnt)
      ctr.insert_symbol(symbol, from_)      
      cnt += 1
    # forward iterate through the timeline
    vs = numpy.zeros([num_exercises, num_sims, num_expl_vars])
    ies = numpy.zeros([num_exercises, num_sims])
    ns = numpy.zeros([num_exercises, num_sims]) # for fees - ignored for present
    normalisation = 1.0/self.__trade.legs()[0].flows()[0].notional()
    ex_cnt = 0
    for time in times:
      to_ = self.__env.relative_date(time)/365.0
      # evolve
      ctr.evolve(from_, to_)
      events = self.__timeline.events(time)
      # evaluate explanatory variables and immediate exercise values
      for event in events:
        # set event on controller
        ctr.set_event(event)
        # evaluate
        if is_exercise_event(event):
          # evaluate underlying  
          underlying = ies[ex_cnt, :]           
          cnt = 0
          for l in self.__trade.legs():
            underlying += ctr.retrieve_symbol("leg"+str(cnt))         
            cnt += 1   
          underlying *= self.__trade.exercise_type()       
          underlying *= normalisation
          # evaluate explanatory variables and numeraire
          ns[ex_cnt, :] = ctr.numeraire(to_)
          vs[ex_cnt, :] = ctr.explanatory_variables(to_)
          ex_cnt += 1
      # evaluate cash flows
      for event in events:
        # set event on controller
        ctr.set_event(event)
        # evaluate
        if is_pay_event(event):
          # evaluate payoff
          cpn = ctr(to_)
          symbol = "leg"+str(event.leg_id())
          leg_pv = ctr.retrieve_symbol(symbol) 
          leg_pv += cpn        
          self.__symbol_listener_(to_, symbol, leg_pv)
          ctr.update_symbol(symbol, leg_pv, to_)                      
      from_ = to_

    # final immediate exercise value
    underlying = ctr.retrieve_symbol("underlying")
    cnt = 0
    for l in self.__trade.legs():
      underlying += ctr.retrieve_symbol("leg"+str(cnt))         
      cnt += 1          
    underlying *= self.__trade.exercise_type()   
    underlying *= normalisation
    # subtract immediate exercise values from final
    for i in range(num_exercises):
      ies[i, :]=underlying-ies[i, :]   
    # perform regression
    self.__fitted_fos = pickup_value_regression(ies, ns, vs)
    # create helper class for dealing with exercise indicator - note number of simulations
    self.__exercise_helper = exercise_helper(self.__model.state().num_sims()) 
      
  def __call__(self, symbol_value_pairs_to_add = None):
    # do regression if required
    if self.__regression_model:
      self.__exercise_boundary_regression(symbol_value_pairs_to_add)
    # create controller
    ctr = controller(self.__trade, self.__model, self.__env, 1.0)
    times = self.__timeline.times()
    from_ = 0.0
    # initialise symbols
    ctr.insert_symbol("underlying", from_)
    ctr.insert_symbol("berm", from_)
    # add extra symbols
    if symbol_value_pairs_to_add:
      for symbol_value_pair in symbol_value_pairs_to_add:
        symbol, value = symbol_value_pair
        ctr.insert_symbol(symbol, value)
    cnt = 0
    for l in self.__trade.legs():
      symbol = "leg"+str(cnt)
      ctr.insert_symbol(symbol, from_)      
      cnt += 1
    # forward iterate through the timeline
    ex_cnt = 0
    for time in times:
      to_ = self.__env.relative_date(time)/365.0
      # evolve
      ctr.evolve(from_, to_)
      events = self.__timeline.events(time)
      # set initial immediate exercise value - sum of all flows before exercise date
      for event in events:
        if is_exercise_event(event):
          # evaluate underlying             
          underlying = ctr.retrieve_symbol("underlying")
          underlying *= 0
          cnt = 0
          for l in self.__trade.legs():
            underlying += ctr.retrieve_symbol("leg"+str(cnt))         
            cnt += 1
          if ex_cnt == 0:
            self.__exercise_helper.set_last_cfs(self.__trade.exercise_type()*underlying)
          self.__symbol_listener_(to_, "underlying", underlying)
      # evaluate cash flows
      for event in events:
        # set event on controller
        ctr.set_event(event)
        # evaluate
        if is_pay_event(event):
          # evaluate payoff
          cpn = ctr(to_)
          symbol = "leg"+str(event.leg_id())
          leg_pv = ctr.retrieve_symbol(symbol) 
          leg_pv += cpn        
          self.__symbol_listener_(to_, symbol, leg_pv)
          ctr.update_symbol(symbol, leg_pv, to_)                   
      # evaluate exercise using regression   
      for event in events:
        # set event on controller
        ctr.set_event(event)
        # evaluate
        if is_exercise_event(event):
          # evaluate underlying             
          underlying = ctr.retrieve_symbol("underlying")
          underlying *= 0
          cnt = 0
          for l in self.__trade.legs():
            underlying += ctr.retrieve_symbol("leg"+str(cnt))         
            cnt += 1
          # explanatory variables and numeraire
          ns = ctr.numeraire(to_) # for fees but not used at present
          vs = ctr.explanatory_variables(to_)
          # evaluate regression
          self.__exercise_helper.update_indicator(to_, vs, self.__fitted_fos[ex_cnt])
          berm = ctr.retrieve_symbol("berm")
          berm = self.__exercise_helper.max(to_, self.__trade.exercise_type()*underlying, berm)
          # update symbols
          ctr.update_symbol("underlying", underlying, to_)
          ctr.update_symbol("berm", berm, to_)
          ex_cnt = ex_cnt+1
      from_ = to_
    # calculate pv
    underlying = ctr.retrieve_symbol("underlying")
    underlying *= 0
    cnt = 0
    for l in self.__trade.legs():
      underlying += ctr.retrieve_symbol("leg"+str(cnt))         
      cnt += 1
    self.__symbol_listener_(to_, "underlying", underlying)
    ctr.update_symbol("underlying", underlying, to_)
    if self.__regression_model:
      berm = ctr.retrieve_symbol("berm")
      berm = self.__exercise_helper.max(to_, self.__trade.exercise_type()*underlying, berm)
      ctr.update_symbol("berm", berm, to_)
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

