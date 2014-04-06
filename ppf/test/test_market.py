import ppf
import math
import unittest

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# surface test suite
#

class surface_tests(unittest.TestCase):
  def test(self):
    from ppf.date_time import date
    from ppf.date_time import months
    from ppf.date_time import Feb, Apr, Jul, Oct, Jan
    from numpy import zeros

    expiries = [
       date(2006, Feb, 11)
     , date(2006, Apr, 11)
     , date(2006, Jul, 11)
     , date(2006, Oct, 11)
     , date(2007, Jan, 11)
     , date(2008, Jan, 11)
     , date(2009, Jan, 11)
     , date(2010, Jan, 11)
     , date(2011, Jan, 11)
     , date(2012, Jan, 11)
     , date(2013, Jan, 11) ]

    tenors = [ months(12), months(24), months(36) ]

    vols = zeros((len(expiries), len(tenors)))
    # expiry, tenor surface                    1y    2y     3y                                
    vols[ 0, 0], vols[ 0, 1], vols[ 0, 2] = 200.00, 76.25, 64.00 # 1m
    vols[ 1, 0], vols[ 1, 1], vols[ 1, 2] =  98.50, 84.75, 69.00 # 3m
    vols[ 2, 0], vols[ 2, 1], vols[ 2, 2] =  98.00, 81.75, 68.00 # 6m
    vols[ 3, 0], vols[ 3, 1], vols[ 3, 2] = 101.25, 82.25, 69.25 # 9m
    vols[ 4, 0], vols[ 4, 1], vols[ 4, 2] = 106.00, 82.00, 69.25 # 1y
    vols[ 5, 0], vols[ 5, 1], vols[ 5, 2] =  78.75, 73.25, 61.25 # 2y
    vols[ 6, 0], vols[ 6, 1], vols[ 6, 2] =  66.25, 59.00, 50.00 # 3y
    vols[ 7, 0], vols[ 7, 1], vols[ 7, 2] =  55.25, 47.75, 41.75 # 4y
    vols[ 8, 0], vols[ 8, 1], vols[ 8, 2] =  44.75, 40.25, 35.50 # 5y
    vols[ 9, 0], vols[ 9, 1], vols[ 9, 2] =  32.00, 30.50, 28.25 # 6y
    vols[10, 0], vols[10, 1], vols[10, 2] =  26.50, 24.25, 24.25 # 7y

    base = date(2006, Jan, 11);
    sig = ppf.market.surface(
         [int(t - base)/365.0 for t in expiries]
       , [m.number_of_months().as_number() for m in tenors]
       , vols)

    tol=1.0e-8
    for i in range(len(expiries)):
      expiry = expiries[i]
      t = int(expiry - base)/365.0
      for j in range(len(tenors)):
        tenor = tenors[j]
        T = tenor.number_of_months().as_number()
        assert math.fabs(sig(t, T) - vols[i, j]) <= tol 

class surface_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(surface_tests, ('test', ))
    unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# driver
#

def suite():
  all_tests = unittest.TestSuite(
      (
        surface_test_suite(),
      ) )

  return all_tests
       
def run_tests():
  runner = unittest.TextTestRunner()
  runner.run(suite())

if __name__ == '__main__':  run_tests()
