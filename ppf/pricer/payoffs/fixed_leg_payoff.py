class fixed_leg_payoff(object):
  def __call__(self, t, controller):    
    event = controller.get_event() 
    flow = event.flow()
    id = event.reset_id()
    obs = flow.observables()[id]
    model = controller.get_model()
    env = controller.get_environment()
    fixed_rate = obs.coupon_rate()
    requestor = model.requestor()
    state = model.state().fill(t, requestor, env)
    cpn = fixed_rate*flow.notional()*flow.year_fraction()*controller.pay_df(t, state)
    return cpn
