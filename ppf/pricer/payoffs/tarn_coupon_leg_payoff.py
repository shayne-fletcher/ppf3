import numpy
from ppf.core import is_last_flow

# max for numpy arrays
max_ = numpy.vectorize(lambda x, y: (x, y)[x < y])
# min for numpy arrays
min_ = numpy.vectorize(lambda x, y: (x, y)[x > y])

class tarn_coupon_leg_payoff(object):
  def __call__(self, t, controller):    
    event = controller.get_event() 
    flow = event.flow()
    id = event.reset_id()
    obs = flow.observables()[id]
    model = controller.get_model()
    env = controller.get_environment()
    adjuvant_table = controller.get_adjuvant_table()
    # lookup 'floor', 'fixed_rate', 'leverage', 'target', 'redemption_floor'
    # and 'redemption_cap'
    floor = adjuvant_table("floor"+str(id), flow.pay_date())
    fixed_rate = adjuvant_table("fixed_rate"+str(id), flow.pay_date())
    leverage = adjuvant_table("leverage"+str(id), flow.pay_date())
    target = adjuvant_table("target"+str(id), flow.pay_date())
    redemption_floor = adjuvant_table("redemption_floor"+str(id), flow.pay_date())
    redemption_cap = adjuvant_table("redemption_cap"+str(id), flow.pay_date())
    requestor = model.requestor()
    state = model.state().fill(t, requestor, env)
    cpn = flow.year_fraction()*max_(floor \
      , fixed_rate+leverage*controller.libor(t, state))
    # retrieve symbol representing target indicator 
    indicator = controller.retrieve_symbol("target_indicator")
    # retrieve symbol representing accrued coupon 
    accrued_cpn = controller.retrieve_symbol("accrued_coupon")
    accrued_cpn += cpn
    # actual coupon assuming a redemption cap and a redemption floor 
    # potentially different from the target
    actual_cpn = model.state().create_variable()
    local_indicator = accrued_cpn >= target
    actual_cpn = (1-indicator)*local_indicator*(cpn-max_(accrued_cpn-redemption_cap,0.0)) \
      +(1-indicator)*(1-local_indicator)*cpn
    leg_id = event.leg_id()
    if is_last_flow(controller.get_trade().legs()[leg_id], flow): 
      actual_cpn += (1-local_indicator)*max_(redemption_floor-accrued_cpn, 0.0)
    actual_cpn *= flow.notional()*controller.pay_df(t, state)

    # update indicator - probability of triggering
    indicator = min_(indicator+local_indicator, 1) 
    # update symbols
    at = env.relative_date(flow.pay_date())/365.0
    controller.update_symbol("accrued_coupon", accrued_cpn, at)
    controller.update_symbol("target_indicator", indicator, at)

    return actual_cpn
