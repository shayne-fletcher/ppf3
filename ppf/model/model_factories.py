from ppf.core import trade_utils
from ppf.model import model
from ppf.model.hull_white import *

class hull_white_lattice_model_factory(object):
  def __call__(self, trd, env, model_args = None):
    '''
    >>> from ppf.date_time import date
    >>> pd = date(2008, 05,  01)
    >>> from ppf.market import environment
    >>> env = environment(pd)
    >>> from ppf.date_time import *
    >>> from ppf.core.pay_receive import *
    >>> from ppf.core.generate_flows import *
    >>> from ppf.core.generate_observables import *
    >>> from ppf.core.generate_exercise_table import *
    >>> from ppf.core.exercise_type import *
    >>> from ppf.core.leg import *
    >>> from ppf.core.trade import *
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
    ...   , pay_currency = "JPY"
    ...   , observables = coupon_observables)
    >>> rcv_flows = generate_flows(
    ...   start  = date(2007, Jun, 29)
    ...   , end  = date(2009, Jun, 29)
    ...   , duration = ppf.date_time.months
    ...   , period = 6
    ...   , shift_method = shift_convention.modified_following
    ...   , basis = "A/360"
    ...   , pay_currency = "JPY"
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
    >>> factory = hull_white_lattice_model_factory()
    >>> hwmodel = factory(structure, env)
    >>> print hwmodel <> None
    True
    '''
    ccy = ppf.core.enforce_single_currency(trd)
    terminal_T = env.relative_date(ppf.core.final_important_date(trd))/365.0
    n = 31
    if model_args <> None and model_args.has_key("num states"):
      n = model_args["num states"]
    std_dev = 4.5
    if model_args <> None and model_args.has_key("num std dev"):
      std_dev = model_args["num std dev"]
    s = lattice.state(ccy, n, std_dev)
    rb = lattice.rollback(ccy)
    f = fill(terminal_T)
    r = requestor()
    return model(r, s, f, rb)

class hull_white_monte_carlo_model_factory(object):
  def __call__(self, trd, env, model_args = None):
    ccy = ppf.core.enforce_single_currency(trd)
    terminal_T = env.relative_date(ppf.core.final_important_date(trd))/365.0
    num_sims = 1000
    if model_args <> None and model_args.has_key("num sims"):
      num_sims = model_args["num sims"]
    seed = 1234
    if model_args <> None and model_args.has_key("seed"):
      seed = model_args["seed"]
    s = monte_carlo.state(num_sims)
    ev = monte_carlo.evolve(ccy, seed)
    f = fill(terminal_T)
    r = requestor()
    ex = None
    id = 0
    if model_args <> None and model_args.has_key("explanatory variables leg id"):
      id = model_args["explanatory variables leg id"]
    if trd.has_exercise_schedule():
      ex = monte_carlo.cle_exercise(trd.legs()[id])
    return model(r, s, f, None, ev, ex)

def _test():
    import doctest
    doctest.testmod()

if __name__ == '__main__':
    _test()
