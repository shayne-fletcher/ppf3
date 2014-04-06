class controller(object):
  def __init__(self, trade, model, env, historical_df = 0):
    self.__trade = trade
    self.__model = model
    self.__env = env
    self.__historical_df = historical_df
    self.__symbol_table = {}
    self.__event = None

  def get_trade(self):
    return self.__trade

  def get_model(self):
    return self.__model

  def get_environment(self):
    return self.__env

  def get_event(self):
    return self.__event

  def set_event(self, event):
    self.__event = event

  def get_adjuvant_table(self):
    leg = self.__trade.legs()[self.__event.leg_id()]
    adjuvant_table = None
    if leg.has_adjuvant_table():
      adjuvant_table = leg.adjuvant_table()
    return adjuvant_table
 
  def insert_symbol(self, name, at):
    self.__symbol_table[name] = (at, self.__model.state().create_variable())

  def update_symbol(self, name, symbol, at):
    self.__symbol_table[name] = (at, symbol)

  def retrieve_symbol(self, name):
    if not self.__symbol_table.has_key(name):
      raise RuntimeError, "name not found in symbol table"
    return self.__symbol_table.get(name)[1]

  def retrieve_symbol_update_time(self, name):
    if not self.__symbol_table.has_key(name):
      raise RuntimeError, "name not found in symbol table"
    return self.__symbol_table.get(name)[0]

  def retrieve_symbols_to_rollback(self, at):
    symbols = []
    for symbol in self.__symbol_table:
      pair = self.__symbol_table.get(symbol)
      if pair[0] > at:
        symbols.append(symbol)
    return symbols

  def pay_df(self, t, state):
    if t < 0:
      historical_df = self.__model.state().create_variable()
      historical_df = self.__historical_df
      return historical_df
    else:
      flow = self.__event.flow()
      fill = self.__model.fill()
      requestor = self.__model.requestor()
      T = self.__env.relative_date(flow.pay_date())/365.0
      return fill.numeraire_rebased_bond(t, T, flow.pay_currency(), self.__env, requestor, state)
    endif

  def libor(self, t, state):
    flow = self.__event.flow()
    id = self.__event.reset_id()
    obs = flow.observables()[id]
    if t < 0:
      fix = obs.fix()
      if fix.is_fixed():
        fixing = self.__model.state().create_variable()
        fixing = fix.value()
        return fixing
      else:
        raise RuntimeError, 'libor in the past with no fixing'
      endif      
    else:
      fill = self.__model.fill()
      requestor = self.__model.requestor()
      return fill.libor(t, obs, self.__env, requestor, state)
    endif

  def swap(self, t, state):
    id = self.__event.reset_id()
    obs = flow.observables()[id]
    if t < 0:
      fix = obs.fix()
      if fix.is_fixed():
        fixing = self.__model.state().create_variable()
        fixing = fix.value()
        return fixing
      else:
        raise RuntimeError, 'libor in the past with no fixing'
      endif      
    else:
      fill = self.__model.fill()
      requestor = self.__model.requestor()
      return fill.swap(t, obs, self.__env, requestor, state)
    endif

  def rollback(self, T, t, symbol):
    requestor = self.__model.requestor()
    state = self.__model.state()
    return self.__model.rollback().rollback(t, T, state, requestor, self.__env, symbol)

  def rollback_max(self, T, t, symbol_one, symbol_two):
    requestor = self.__model.requestor()
    state = self.__model.state()
    res1 = self.__model.rollback().rollback(t, T, state, requestor, self.__env, symbol_one)
    res2 = self.__model.rollback().rollback_max(t, T, state, requestor, self.__env, symbol_two-symbol_one)
    return res1+res2

  def evolve(self, t, T):
    requestor = self.__model.requestor()
    state = self.__model.state()
    self.__model.evolve().evolve(t, T, state, requestor, self.__env)

  def numeraire(self, t):
    if t < 0:
      raise RuntimeError, "attempting to call 'numeraire' in the past"
    fill = self.__model.fill()
    requestor = self.__model.requestor()
    state = self.__model.state().fill(t, requestor, self.__env)
    return fill.numeraire(t, self.__event.pay_currency(), self.__env, requestor, state)

  def explanatory_variables(self, t):
    if t < 0:
      raise RuntimeError, "attempting to call 'explanatory_variables' in the past"
    fill = self.__model.fill()
    requestor = self.__model.requestor()
    state = self.__model.state().fill(t, requestor, self.__env)
    exercise = self.__model.exercise()
    return exercise(t, fill, state, requestor, self.__env)

  def __call__(self, t):
    leg = self.__trade.legs()[self.__event.leg_id()]
    payoff = leg.payoff()
    pay_rcv = leg.pay_receive()
    return pay_rcv*payoff(t, self) 
          
