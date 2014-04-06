import ppf
import math
import unittest

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# black-scholes suite
#

class black_scholes_tests(unittest.TestCase):
  def test_call(self):
    black_scholes = ppf.core.black_scholes
    CALL = ppf.core.CALL

    v = ppf.core.black_scholes(S=42., K=40., r=0.1, sig= 0.2, T=0.5, CP=CALL)
    assert math.fabs(v - 4.75942193531) < 0.0001

  def test_put(self):
    black_scholes = ppf.core.black_scholes
    PUT = ppf.core.PUT

    v = ppf.core.black_scholes(S=42., K=40., r=0.1, sig= 0.2, T=0.5, CP=PUT)
    assert math.fabs(v - 0.808598915338) < 0.0001

class black_scholes_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(black_scholes_tests, ('test_call', 'test_put'))
    unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# libor rate suite
#

class libor_rate_tests(unittest.TestCase):
  def test(self):
    from ppf.date_time import date
    Jun = ppf.date_time.Jun
    periods = ppf.core.generate_date_tuples(
         start = date(2007, Jun, 29)
       , end   = date(2027, Jun, 29)
       , duration = ppf.date_time.months
       , period = 3
       , shift_method = ppf.date_time.shift_convention.modified_following
       , basis = "ACT/360")
    attributes={}
    t = date(2007, Jun, 29) #valuation date
    import math
    from ppf.math.interpolation import loglinear
    times = range(0, 22)
    P = loglinear(times, [math.exp(-0.05*T) for T in times])
    libor_table= []
    for i in range(len(periods)):
      reset = periods[i]
      reset_date = reset[0]
      projection_start, projection_until = reset
      libor_table.append(
        ppf.core.libor_rate(attributes
                          , i #flow id
                          , i #reset id
                          , reset_date
                          , "JPY"
                          , projection_start
                          , projection_until
                          , ppf.date_time.basis_act_360
                          , ppf.core.fixing(False)))
    forwards = [l.forward(t, P) for l in libor_table]
    for l in libor_table:
      Ts, Te = (int(l.proj_start_date() - t)/365.0
              , int(l.proj_end_date()   - t)/365.0)
      Ps, Pe = (P(Ts), P(Te))
      alpha = ppf.date_time.year_fraction(
        l.proj_start_date(), l.proj_end_date(), l.proj_basis())
      fwd = (Ps/Pe - 1)/alpha
      assert(fwd == l.forward(t, P))

class libor_rate_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(libor_rate_tests, ('test', ))
    unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# swap rate suite
#

class swap_rate_tests(unittest.TestCase):
  def test(self):
    from ppf.core import swap_rate
    from ppf.market import curve
    from ppf.math import loglinear
    from ppf.date_time            \
         import date              \
              , shift             \
              , shift_convention  \
              , months            \
              , years             \
              , basis_act_360     \
              , basis_act_365

    May = ppf.date_time.May
    modified_following = shift_convention.modified_following

    t = date(2005, May, 01)
    spot = date(2005, May, 03)
    maturity = shift(spot + years(10), modified_following)

    attributes = {}

    attributes["fixed-pay-period"] = 1
    attributes["fixed-pay-period-duration"] = years
    attributes["fixed-pay-basis"] = basis_act_360
    attributes["fixed-pay-holiday-centers"] = None
    attributes["fixed-shift-convention"] = modified_following

    attributes["float-pay-period"] = 6
    attributes["float-pay-period-duration"] = months
    attributes["float-pay-basis"] = basis_act_365
    attributes["float-pay-holiday-centers"] = None
    attributes["float-shift-convention"] = modified_following

    attributes["index-basis"] = basis_act_365
    attributes["index-holiday-centers"] = None
    attributes["index-shift-convention"] = modified_following

    #10y swap rate
    rate = swap_rate(
        attributes
      , 0 #flow id
      , 0 #reset id
      , spot #reset date
      , "GBP" #reset ccy
      , spot #proj start
      , maturity #proj end
      , None #fixing
      )

    times = range(0, 13)#12 years on the curve
    P = curve(times, [math.exp(-0.05*T) for T in times], loglinear)
    assert(math.fabs(0.0495099316847 - rate.forward(t, P)) < 1.0E-4)

class swap_rate_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(swap_rate_tests, ('test', ))
    unittest.TestSuite.__init__(self, tests)
  
#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# driver
#

def suite():
  all_tests = unittest.TestSuite(
      (
          black_scholes_test_suite()
        , libor_rate_test_suite()
        , swap_rate_test_suite()
      ) )

  return all_tests
       
def run_tests():
  runner = unittest.TextTestRunner()
  runner.run(suite())

if __name__ == '__main__':  run_tests()
