import utils

class BlackScholesServer(object):
  _public_methods_ = ["OptionPrice"]
  _reg_progid_ = "ppf.black_scholes"
  _reg_clsid_ = "{14B40B3E-DC9A-4E07-A512-F65DA07BDC09}"

  def OptionPrice(self, spot, strike, rate, vol, time, call_put):
     from ppf.core import black_scholes
     try:
       return black_scholes(
                 S=spot, K=strike, r=rate, sig=vol, T=time, CP=call_put)
     except RuntimeError, e:
       ppf.com.utils.raise_com_exception(e)

if __name__ == "__main__":
  utils.register_com_class(BlackScholesServer)
