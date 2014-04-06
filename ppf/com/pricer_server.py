import ppf.model
import ppf.pricer
import utils

class PricerServer(object):
  _reg_progid_ = "ppf.pricer"
  _reg_clsid_ = "{08632905-0B63-45B5-B388-30C73CAE611C}"
  _public_methods_ = \
  [
      "CreateHullWhiteLatticePricer"
                    , "InvokePricer"
  ]
  _pricers = {}

  retrieve = staticmethod(
       lambda tag, which :
         utils.retrieve('pricer_server', 'PricerServer', tag, which))

  def CreateHullWhiteLatticePricer(
      self
      , tag
      , trade_id
      , env_id
      , num_states
      , num_std_dev):
    try:
      from trade_server import TradeServer
      from market_server import MarketServer
      trade = TradeServer.retrieve(trade_id, 'trades')
      env   = MarketServer.retrieve(env_id, 'environments')
      model_args = {"num states": num_states, "num std dev": num_std_dev} 
      factory = ppf.model.hull_white_lattice_model_factory()
      model = factory(trade, env, model_args)
      pricer = ppf.pricer.lattice_pricer(trade, model, env, None)
      PricerServer._pricers[tag] = pricer
      return tag
    except RuntimeError, e: ppf.com.utils.raise_com_exception(e)

  def InvokePricer(self, tag):
    try:
      return PricerServer.retrieve(tag, 'pricers').__call__()
    except RuntimeError, e: utils.raise_com_exception(e)

if __name__ == "__main__": utils.register_com_class(PricerServer)
