import unittest

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# imm date calculation suite
#

class imm_tests(unittest.TestCase):
  def test_nth_imm_of_year(self):
    from ppf.date_time import nth_imm_of_year, date, months_of_year
    imm = nth_imm_of_year
    Mar, Jun, Sep, Dec = \
         months_of_year.Mar, months_of_year.Jun, \
         months_of_year.Sep, months_of_year.Dec
    imm_dates = [imm(x).get_date(2005) for x in
                   [imm.first, imm.second, imm.third, imm.fourth]]
    assert imm_dates == [ \
          date(2005, Mar, 16)
        , date(2005, Jun, 15)
        , date(2005, Sep, 21)
        , date(2005, Dec, 21)]
    
  def test_first_imm_before(self):
    from ppf.date_time import first_imm_before, date, months_of_year
    Jun = months_of_year.Jun
    assert first_imm_before(date(2007, Jun, 27)) == date(2007, Jun, 20)

  def test_first_imm_after(self):
    from ppf.date_time import first_imm_after, date, months_of_year
    Jun, Sep = months_of_year.Jun, months_of_year.Sep
    assert first_imm_after(date(2007, Jun, 27)) == date(2007, Sep, 19)
  
class imm_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(imm_tests, ('test_nth_imm_of_year'
                          , 'test_first_imm_after'
                          , 'test_first_imm_before'))
    unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# business day suite
#

class business_day_tests(unittest.TestCase):
    def test(self):
      from ppf.date_time import date, months_of_year, is_business_day
      Jun = months_of_year.Jun
      assert is_business_day(date(2007, Jun, 27))
      assert not is_business_day(date(2007, Jun, 30))

class business_day_test_suite(unittest.TestSuite):
    def __init__(self):
      tests = map(business_day_tests, ('test',))
      unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# driver
#

def suite():
  all_tests = unittest.TestSuite(
      (
          imm_test_suite()
        , business_day_test_suite()
      ) )

  return all_tests
       
def run_tests():
  runner = unittest.TextTestRunner()
  runner.run(suite())

if __name__ == '__main__':  run_tests()
