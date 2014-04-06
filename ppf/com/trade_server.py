import ppf.core
import ppf.pricer.payoffs
import ppf.date_time
import utils

class TradeServer(object):
  _reg_progid_ = "ppf.trade"
  _reg_clsid_ = "{E33DA322-B011-4FE9-8AB9-87A964EDD046}"
  _public_methods_ = \
   [
        "GenerateFixedCouponObservables"
            , "GenerateLiborObservables"
                       , "GenerateFlows"
               , "GenerateAdjuvantTable"
            , "GenerateExerciseSchedule"
                           , "CreateLeg"
                         , "CreateTrade"
  ]
  _observables = {}
  _flows       = {}
  _adjuvants   = {}
  _legs        = {}
  _exercises   = {}
  _trades      = {}

  retrieve = staticmethod(
       lambda tag, which :
         utils.retrieve('trade_server', 'TradeServer', tag, which))

  def GenerateFixedCouponObservables(
      self
      , tag
      , start
      , end
      , roll_period
      , roll_duration
      , reset_currency
      , coupon_shift_method
      , coupon_rate):
    try:
      observables = \
       ppf.core.generate_fixed_coupon_observables(
            start=utils.to_ppf_date(start)
          , end=utils.to_ppf_date(end)
          , roll_period=roll_period
          , roll_duration=eval("ppf.date_time."+roll_duration)
          , reset_currency=reset_currency
          , coupon_shift_method=
              eval("ppf.date_time.shift_convention."+coupon_shift_method)
          , coupon_rate=coupon_rate)
      TradeServer._observables[tag] = observables
      return tag
    except RuntimeError, e: utils.raise_com_exception(e)

  def GenerateLiborObservables(
      self
      , tag
      , start
      , end
      , roll_period
      , roll_duration
      , reset_period
      , reset_duration
      , reset_currency
      , reset_basis
      , reset_shift_method):
    try:
      observables = \
        ppf.core.generate_libor_observables(
            start=utils.to_ppf_date(start)
          , end=utils.to_ppf_date(end)
          , roll_period=roll_period
          , roll_duration = eval("ppf.date_time."+roll_duration)
          , reset_period = reset_period
          , reset_duration = eval("ppf.date_time."+reset_duration)
          , tenor_period = reset_period
          , tenor_duration = eval("ppf.date_time."+reset_duration)
          , reset_currency=reset_currency
          , reset_basis = eval("ppf.date_time."+reset_basis)
          , reset_shift_method=eval( \
             "ppf.date_time.shift_convention."+reset_shift_method)
          , reset_lag = 0)
      TradeServer._observables[tag] = observables
      return tag
    except RuntimeError, e: utils.raise_com_exception(e)

  def GenerateFlows(
      self
      , tag
      , start
      , end
      , period
      , duration
      , pay_currency
      , pay_shift_method
      , accrual_basis
      , observables):
    try:
      flows = ppf.core.generate_flows(
          start=utils.to_ppf_date(start)
          , end=utils.to_ppf_date(end)
          , duration=eval("ppf.date_time."+duration)
          , period=period
          , pay_shift_method=eval(\
              "ppf.date_time.shift_convention."+pay_shift_method)
          , pay_currency=pay_currency
          , accrual_basis=eval("ppf.date_time."+accrual_basis)
          , observables=TradeServer.retrieve(observables, 'observables'))
      TradeServer._flows[tag] = flows
      return tag
    except RuntimeError, e: utils.raise_com_exception(e)

  def GenerateAdjuvantTable(
      self
      , tag
      , items
      , tens
      , vals
      , start
      , roll_period
      , roll_duration
      , shift_method):
    try:
      import numpy
      adjuvants = \
         ppf.core.generate_adjuvant_table(
              items[1:]
            , [int(t) for t in tens[1:]]
            , numpy.array([x[1:len(vals[0])] for x in vals[1:]])
            , utils.to_ppf_date(start)
            , rol_period=roll_period
            , roll_duration=eval("ppf.date_time."+roll_duration)
            , shift_method=eval(\
                 "ppf.date_time.shift_convention."+shift_method))
      TradeServer._adjuvants[tag] = adjuvants
      return tag
    except RuntimeError, e: utils.raise_com_exception(e)

  def GenerateExerciseSchedule(
      self
      , tag
      , start
      , end
      , period
      , duration
      , shift_method):
    try:
      sched = \
        ppf.core.generate_exercise_table(
            start = utils.to_ppf_date(start)
          , end = utils.to_ppf_date(end)
          , period = period
          , duration = eval("ppf.date_time."+duration)
          , shift_method = eval("ppf.date_time.shift_convention."+shift_method))
      TradeServer._exercises[tag] = sched
      return tag
    except RuntimeError, e:
      utils.raise_com_exception(e)
    
  def CreateLeg(
    self
    , tag
    , flows
    , pay_or_receive
    , adjuvant_table
    , payoff):
    try:
      adjuvants = None
      if adjuvant_table:
        adjuvants = TradeServer.retrieve(adjuvant_table, 'adjuvants')
      leg = \
          ppf.core.leg(
             TradeServer.retrieve(flows, 'flows')
             , eval("ppf.core."+pay_or_receive)
             , adjuvants
             , eval("ppf.pricer.payoffs."+payoff)())
      TradeServer._legs[tag] = leg
      return tag
    except RuntimeError, e: utils.raise_com_exception(e)

  def CreateTrade(
    self
    , tag
    , legs
    , exercise_sched
    , exercise_type):
    try:
      tl = [TradeServer.retrieve(l, 'legs') for l in legs[1:]]
      if exercise_sched:
        exercises = TradeServer.retrieve(exercise_sched, 'exercises')
        if not exercise_type:
          raise RuntimeError, "missing exercise type"
        call_cancel = eval("ppf.core.exercise_type."+exercise_type)
        trade = ppf.core.trade(tl, (exercises, call_cancel))
      else:
        trade = ppf.core.trade(tl, None)
      TradeServer._trades[tag] = trade
      return tag
    except RuntimeError, e: utils.raise_com_exception(e)
    
if __name__ == "__main__": utils.register_com_class(TradeServer)
