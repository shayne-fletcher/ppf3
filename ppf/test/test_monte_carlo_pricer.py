import ppf, math, numpy, unittest

# max for numpy arrays
max_ = numpy.vectorize(lambda x, y: (x, y)[x < y])

def _assert_seq_close(a, b, tol=1.0e-8):
  assert (len(a) == len(b)) and \
  not [l for l in [math.fabs(x - y) <= tol for (x, y) in zip(a, b)] if not l]

def _create_environment():
  from ppf.date_time import date
  pd = date(2006, 12, 29)
  env = ppf.market.environment(pd)
  times = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0]
  factors = [math.exp(-0.05*t) for t in times]
  env.add_curve("zc.disc.usd"
     , ppf.market.curve(times, factors, ppf.math.interpolation.loglinear))
  expiries = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0]
  tenors = [0, 90]
  values = numpy.zeros((14, 2))  
  values.fill(0.001)#(0.00001)
  env.add_surface("ve.term.usd.hw"
                 , ppf.market.surface(expiries, tenors, values))
  env.add_constant("cv.mr.usd.hw", 0.01)
  return env
  
def _create_tarn_funding_leg():
  from ppf.date_time \
       import date, shift_convention, modified_following, basis_act_360, months
  libor_observables = ppf.core.generate_libor_observables(\
    start  = date(2007, 06, 29)\
    , end  = date(2010, 06, 29)\
    , roll_period = 6\
    , roll_duration = ppf.date_time.months\
    , reset_period = 6\
    , reset_duration = ppf.date_time.months\
    , reset_currency = "USD"\
    , reset_basis = basis_act_360\
    , reset_shift_method = shift_convention.modified_following)  

  adjuvant_table = ppf.core.generate_adjuvant_table(\
    keys = ["spread0"]\
    , tenors = [48]\
    , values = numpy.array([[0.0]])\
    , shift_method = shift_convention.modified_following\
    , start_date = date(2007, 06, 29)) 

  flows = ppf.core.generate_flows(\
    start  = date(2007, 06, 29)\
    , end  = date(2010, 06, 29)\
    , duration = ppf.date_time.months\
    , period = 6\
    , pay_shift_method = shift_convention.modified_following\
    , pay_currency = "USD"\
    , basis = "A/360"\
    , observables = libor_observables)

  leg = ppf.core.leg(flows, ppf.core.RECEIVE, adjuvant_table\
    , ppf.pricer.payoffs.tarn_funding_leg_payoff())
  return leg

def _create_tarn_coupon_leg(floor, fixed_rate, leverage, target, redemption_floor\
   , redemption_cap):
  from ppf.date_time \
       import date, shift_convention, modified_following, basis_act_360, months
  libor_observables = ppf.core.generate_libor_observables(\
    start  = date(2007, 06, 29)\
    , end  = date(2010, 06, 29)\
    , roll_period = 6\
    , roll_duration = ppf.date_time.months\
    , reset_period = 6\
    , reset_duration = ppf.date_time.months\
    , reset_currency = "USD"\
    , reset_basis = basis_act_360\
    , reset_shift_method = shift_convention.modified_following)  

  adjuvant_table = ppf.core.generate_adjuvant_table(\
    keys = ["floor0", "fixed_rate0", "leverage0", "target0", "redemption_floor0"\
      , "redemption_cap0"]\
    , tenors = [48]\
    , values = numpy.array([[floor], [fixed_rate], [leverage], [target]\
      , [redemption_floor], [redemption_cap]])\
    , shift_method = shift_convention.modified_following\
    , start_date = date(2007, 06, 29)) 

  flows = ppf.core.generate_flows(\
    start  = date(2007, 06, 29)\
    , end  = date(2010, 06, 29)\
    , duration = ppf.date_time.months\
    , period = 6\
    , pay_shift_method = shift_convention.modified_following\
    , pay_currency = "USD"\
    , basis = "A/360"\
    , observables = libor_observables)

  leg = ppf.core.leg(flows, ppf.core.PAY, adjuvant_table\
    , ppf.pricer.payoffs.tarn_coupon_leg_payoff())
  return leg

def _create_pricer(trade, env, listener = None):
  model_args = {"num sims": 5000, "seed": 1234} 
  factory = ppf.model.hull_white_monte_carlo_model_factory()
  model = factory(trade, env, model_args)
  pricer = ppf.pricer.monte_carlo_pricer(trade, model, env, listener)
  return pricer

def _exotic_first_flow_pv(leg, env):
  f = leg.flows()[0]
  obs = f.observables()[0]
  key = "zc.disc."+f.pay_currency()
  curve = env.retrieve_curve(key)
  T = env.relative_date(f.pay_date())/365.0
  dfT = curve(T)
  id = 0
  adjuvant_table = leg.adjuvant_table()
  floor = adjuvant_table("floor"+str(id), f.pay_date())
  fixed_rate = adjuvant_table("fixed_rate"+str(id), f.pay_date())
  leverage = adjuvant_table("leverage"+str(id), f.pay_date())
  fwd = obs.forward(env.pricing_date(), curve)
  pv = max(fixed_rate+leverage*fwd, floor)*f.notional()*f.year_fraction()*dfT
  return pv*leg.pay_receive()

def _funding_first_flow_pv(leg, env):
  f = leg.flows()[0]
  obs = f.observables()[0]
  key = "zc.disc."+f.pay_currency()
  curve = env.retrieve_curve(key)
  T = env.relative_date(f.pay_date())/365.0
  dfT = curve(T)
  pv = obs.forward(env.pricing_date(), curve)*f.notional()*f.year_fraction()*dfT
  return pv*leg.pay_receive()    

class tarn_tests(unittest.TestCase):
  def no_trigger_limit_test(self):
    floor = -100
    fixed_rate = 0.0
    leverage = 1.0
    target = 10000
    redemption_floor = -100
    redemption_cap = 100
    coupon_leg = _create_tarn_coupon_leg(floor, fixed_rate, leverage\
     , target, redemption_floor, redemption_cap)
    funding_leg = _create_tarn_funding_leg()
    env = _create_environment()
    tarn = ppf.core.trade((funding_leg, coupon_leg)) # note the ordering
    pricer = _create_pricer(tarn, env)
    symbol_value_pairs_to_add = []
    symbol_value_pairs_to_add.append(("accrued_coupon", numpy.zeros(5000)))
    symbol_value_pairs_to_add.append(("target_indicator", numpy.zeros(5000)))
    actual = pricer(symbol_value_pairs_to_add)
    _assert_seq_close([actual/10000000], [0.0], 1.0e-4)

  def trigger_after_first_flow_test(self):
    floor = -100
    fixed_rate = 0.05
    leverage = 0.0
    target = 0.0
    redemption_floor = -100
    redemption_cap = 100
    coupon_leg = _create_tarn_coupon_leg(floor, fixed_rate, leverage\
     , target, redemption_floor, redemption_cap)
    funding_leg = _create_tarn_funding_leg()
    env = _create_environment()
    tarn = ppf.core.trade((funding_leg, coupon_leg)) # note the ordering
    pricer = _create_pricer(tarn, env)
    symbol_value_pairs_to_add = []
    symbol_value_pairs_to_add.append(("accrued_coupon", numpy.zeros(5000)))
    symbol_value_pairs_to_add.append(("target_indicator", numpy.zeros(5000)))
    actual = pricer(symbol_value_pairs_to_add)
    expected = _exotic_first_flow_pv(coupon_leg, env)\
      +_funding_first_flow_pv(funding_leg, env)
    #print actual, expected, (actual-expected)/10000000
    _assert_seq_close([actual/10000000], [expected/10000000], 1.0e-4)

  def monotonic_with_target_test(self):
    floor = -100
    fixed_rate = 0.025
    leverage = 2.0
    redemption_floor = -100
    redemption_cap = 100
    prev = 1 # out-of-the-money
    targets = [0.075, 0.1, 0.125, 0.15, 0.175, 0.2]
    for target in targets:
      coupon_leg = _create_tarn_coupon_leg(floor, fixed_rate, leverage\
       , target, redemption_floor, redemption_cap)
      funding_leg = _create_tarn_funding_leg()
      env = _create_environment()
      tarn = ppf.core.trade((funding_leg, coupon_leg)) # note the ordering
      pricer = _create_pricer(tarn, env)
      symbol_value_pairs_to_add = []
      symbol_value_pairs_to_add.append(("accrued_coupon", numpy.zeros(5000)))
      symbol_value_pairs_to_add.append(("target_indicator", numpy.zeros(5000)))
      curr = pricer(symbol_value_pairs_to_add)
      assert(curr < prev)
      prev = curr

def _create_funding_leg():
  from ppf.date_time \
       import date, shift_convention, modified_following, basis_act_360, months
  libor_observables = ppf.core.generate_libor_observables(\
    start  = date(2007, 06, 29)\
    , end  = date(2010, 06, 29)\
    , roll_period = 6\
    , roll_duration = ppf.date_time.months\
    , reset_period = 6\
    , reset_duration = ppf.date_time.months\
    , reset_currency = "USD"\
    , reset_basis = basis_act_360\
    , reset_shift_method = shift_convention.modified_following)  

  adjuvant_table = ppf.core.generate_adjuvant_table(\
    keys = ["spread0"]\
    , tenors = [48]\
    , values = numpy.array([[0.0]])\
    , shift_method = shift_convention.modified_following\
    , start_date = date(2007, 06, 29)) 

  flows = ppf.core.generate_flows(\
    start  = date(2007, 06, 29)\
    , end  = date(2010, 06, 29)\
    , duration = ppf.date_time.months\
    , period = 6\
    , pay_shift_method = shift_convention.modified_following\
    , pay_currency = "USD"\
    , accrual_basis = basis_act_360\
    , observables = libor_observables)

  leg = ppf.core.leg(flows, ppf.core.RECEIVE, adjuvant_table\
    , ppf.pricer.payoffs.float_leg_payoff())
  return leg

def _create_fixed_leg(coupon = None):
  from ppf.date_time \
       import date, shift_convention, modified_following, basis_act_360, months
  cpn = 0.06
  if coupon <> None:
    cpn = coupon
  coupon_observables = ppf.core.generate_fixed_coupon_observables(\
     start  = date(2007, 06, 29)\
    , end  = date(2010, 06, 29)\
    , roll_period = 6\
    , reset_currency = "USD"\
    , coupon_shift_method = shift_convention.modified_following\
    , coupon_rate = cpn)  

  flows = ppf.core.generate_flows(\
      start  = date(2007, 06, 29)\
    , end  = date(2010, 06, 29)\
    , duration = ppf.date_time.months\
    , period = 6\
    , pay_shift_method = shift_convention.modified_following\
    , pay_currency = "USD"\
    , accrual_basis = basis_act_360
    , observables = coupon_observables)

  leg = ppf.core.leg(flows, ppf.core.PAY, None\
    , ppf.pricer.payoffs.fixed_leg_payoff())
  return leg 

def _create_exercise_schedule(sd = ppf.date_time.date(2007, 06, 29)\
                              , ed = ppf.date_time.date(2009, 06, 29)):
  from ppf.date_time \
       import date, shift_convention, modified_following, basis_act_360, months
  sched = ppf.core.generate_exercise_table(
    start  = sd
    , end  = ed
    , period = 1
    , duration = ppf.date_time.years
    , shift_method = shift_convention.modified_following
    , fee_currency = "USD")
  return sched

def _fixed_leg_pv(leg, env):
  pv = 0.0
  for f in leg.flows():
    obs = f.observables()[0]
    key = "zc.disc."+f.pay_currency()
    curve = env.retrieve_curve(key)
    T = env.relative_date(f.pay_date())/365.0
    dfT = curve(T)
    pv += obs.coupon_rate()*f.notional()*f.year_fraction()*dfT
  return pv*leg.pay_receive()

def _funding_leg_pv(leg, env):
  pv = 0.0
  for f in leg.flows():
    obs = f.observables()[0]
    key = "zc.disc."+f.pay_currency()
    curve = env.retrieve_curve(key)
    T = env.relative_date(f.pay_date())/365.0
    dfT = curve(T)
    pv += obs.forward(env.pricing_date(), curve)*f.notional()*f.year_fraction()*dfT
  return pv*leg.pay_receive()

def _create_callable_pricer(trade, env, listener = None):
  regression_model_args = {"num sims": 3000, "seed": 12345, "explanatory variables leg id": 0} 
  factory = ppf.model.hull_white_monte_carlo_model_factory()
  regression_model = factory(trade, env, regression_model_args)
  model_args = {"num sims": 6000, "seed": 1234, "explanatory variables leg id": 0} 
  model = factory(trade, env, model_args)
  pricer = ppf.pricer.monte_carlo_pricer(trade, model, env, listener, regression_model)
  return pricer

class bermudan_tests(unittest.TestCase):
  def test_value(self):
    fixed_leg = _create_fixed_leg()
    funding_leg = _create_funding_leg()
    ex_sch = _create_exercise_schedule()
    env = _create_environment() 
    berm = ppf.core.trade((fixed_leg, funding_leg), (ex_sch, ppf.core.exercise_type.callable))   
    pricer = _create_callable_pricer(berm, env)
    actual = pricer()
    europeans = []
    for exercise in ex_sch:
      european_ex_sch = _create_exercise_schedule(exercise.exercise_date(), exercise.exercise_date())
      european = ppf.core.trade((fixed_leg, funding_leg), (european_ex_sch, ppf.core.exercise_type.callable))   
      pricer = _create_callable_pricer(european, env)
      europeans.append(pricer())
    for european in europeans:
      #print actual, european
      assert(actual >= european)  

class moneyness_tests(unittest.TestCase):
  def deep_in_the_money_test(self):
    fixed_leg = _create_fixed_leg(-1.0)
    funding_leg = _create_funding_leg()
    ex_sch = _create_exercise_schedule()
    env = _create_environment() 
    berm = ppf.core.trade((fixed_leg, funding_leg), (ex_sch, ppf.core.exercise_type.callable))   
    pricer = _create_callable_pricer(berm, env)
    actual = pricer()
    expected = _fixed_leg_pv(fixed_leg, env)+_funding_leg_pv(funding_leg, env)
    _assert_seq_close([actual/10000000], [expected/10000000], 3.0e-4)
  def deep_out_the_money_test(self):
    fixed_leg = _create_fixed_leg(1.0)
    funding_leg = _create_funding_leg()
    ex_sch = _create_exercise_schedule()
    env = _create_environment() 
    berm = ppf.core.trade((fixed_leg, funding_leg), (ex_sch, ppf.core.exercise_type.callable))   
    pricer = _create_callable_pricer(berm, env)
    actual = pricer()
    expected = 0.0
    _assert_seq_close([actual/10000000], [expected/10000000], 3.0e-4)    

class monte_carlo_pricer_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(tarn_tests,('no_trigger_limit_test','trigger_after_first_flow_test'\
                            ,'monotonic_with_target_test')) + \
            map(bermudan_tests,('test_value',)) + \
            map(moneyness_tests,('deep_in_the_money_test','deep_out_the_money_test'))

    unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# driver
#

def suite():
  all_tests = unittest.TestSuite(
      (
         monte_carlo_pricer_test_suite()
       , 
      ) )

  return all_tests
       
def run_tests():
  runner = unittest.TextTestRunner()
  runner.run(suite())

if __name__ == '__main__':  run_tests()
