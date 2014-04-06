import ppf.market
import utils

class MarketServer(object):
  _reg_progid_ = "ppf.market"
  _reg_clsid_ = "{CAFAEEDF-E876-4DD6-9B6F-7038EDA25BCD}"
  _public_methods_ = \
  [
      "CreateEnvironment"
     , "EraseEnvironment"
             , "AddCurve"
           , "AddSurface"
          , "AddConstant"
             , "ListKeys"
  ]
  _environments = {}

  retrieve = staticmethod(
       lambda tag, which :
         utils.retrieve('market_server', 'MarketServer', tag, which))

  def CreateEnvironment(self, tag, t):
     try:
       MarketServer._environments[tag] = \
          ppf.market.environment(utils.to_ppf_date(t))
       return tag
     except RuntimeError, e: utils.raise_com_exception(e)

  def AddCurve(self, tag, name, curve, interp):
    try:
      import ppf.math.interpolation
      interp = eval("ppf.math.interpolation."+interp)
      times, factors = [x[1] for x in curve[1:]],[x[2] for x in curve[1:]]
      MarketServer.retrieve(tag, 'environments').add_curve(
          str(name), ppf.market.curve(times, factors, interp))
    except RuntimeError, e: utils.raise_com_exception(e)

  def AddConstant(self, tag, name, value):
    try:
      MarketServer.retrieve(tag, 'environments').add_constant(
        str(name), value)
    except RuntimeError, e: utils.raise_com_exception(e)

  def AddSurface(self, tag, name, expiries, tenors, values):
    try:
      import numpy
      exp, ten = expiries[1:], tenors[1:]
      surface = [x[1:] for x in values[1:]]
      MarketServer.retrieve(tag,'environments').add_surface(
        str(name), ppf.market.surface(exp, ten, numpy.array(surface)))
    except RuntimeError, e: utils.raise_com_exception(e)

if __name__ == "__main__": utils.register_com_class(MarketServer)
