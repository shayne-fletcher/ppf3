import ppf
import unittest

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# bound suite
#

class bound_tests(unittest.TestCase):
  def test_lower_bound(self):
    values = [1, 2, 3]
    lower_bound = ppf.utility.lower_bound
    assert lower_bound(0.0, values) == 0
    assert lower_bound(1.0, values) == 0
    assert lower_bound(1.5, values) == 1
    assert lower_bound(3.1, values) == 3

  def test_upper_bound(self):
    values = [1, 2, 3, 3]
    upper_bound = ppf.utility.upper_bound
    assert upper_bound(0.0, values) == 0
    assert upper_bound(3.0, values) == 4
    assert upper_bound(4.0, values) == 4

  def test_equal_range(self):
    values = [1, 2, 3, 3, 4]
    equal_range = ppf.utility.equal_range
    assert equal_range(1.4, values) == (1, 1)
    assert equal_range(3.0, values) == (2, 4)

  def test_bound(self):
    bound = ppf.utility.bound
    values = [1, 2, 3]
    i, j = bound(1.5, values)
    assert i == j -1 and values[i] <= 1.5 <= values[j]
    i, j = bound(2.0, [1, 2, 3])
    assert i == j -1 and values[i] <= 2.0 <= values[j]
    self.assertRaises(RuntimeError, bound, 4, values)

  def test_bound_ci(self):
    bound = ppf.utility.bound
    values = ['ape', 'Apple', 'caNada']
    i, j = bound('bananana', values
                 , lambda x, y: x.lower() < y.lower())
    assert i == j -1 and values[i].lower() <= 'banana' <= values[j].lower()

class bound_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(bound_tests,
                ('test_lower_bound',
                 'test_upper_bound',
                 'test_equal_range',
                 'test_bound',
                 'test_bound_ci'
                 )
                )
    unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# driver
#

def suite():
  all_tests = unittest.TestSuite(
      (
        bound_test_suite()
      ) )

  return all_tests
       
def run_tests():
  runner = unittest.TextTestRunner()
  runner.run(suite())

if __name__ == '__main__':  run_tests()
