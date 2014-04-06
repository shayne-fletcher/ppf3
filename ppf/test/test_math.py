import ppf
import math
import numpy
import random
import unittest

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# interpolation suite
#

class linear_interpolation_tests(unittest.TestCase):
  def test(self):
    abscissae = [float(x) for x in range(10) if x % 2]
    ordinates = [2*x + 1 for x in abscissae]
    f = ppf.math.linear(abscissae, ordinates)
    for i in [x for x in range(1, 10) if not x%2]:
      assert f(i) == 2.*i + 1
    self.assertRaises(RuntimeError, f,  0)
    self.assertRaises(RuntimeError, f, 10)

class cubic_spline_interpolation_tests(unittest.TestCase):
  def test_list(self):
    pi, sin = math.pi, math.sin
    abscissae = [0,      pi/2,      pi     ]
    ordinates = [sin(0), sin(pi/2), sin(pi)]
    f = ppf.math.cubic_spline(abscissae, ordinates)
    for i in range(0, 5):
      x = pi*i/4
      assert math.fabs(f(x) - math.sin(x)) <= 0.05     

  def test_array(self):
    pi, sin = math.pi, math.sin
    abscissae = numpy.zeros(3)
    ordinates = numpy.zeros(3)
    abscissae[0], abscissae[1], abscissae[2] = 0, pi/2, pi
    ordinates[0], ordinates[1], ordinates[2] = sin(0), sin(pi/2), sin(pi)
    f = ppf.math.cubic_spline(abscissae, ordinates)
    for i in range(0, 5):
      x = pi*i/4
      assert math.fabs(f(x) - math.sin(x)) <= 0.05     

class interpolation_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(linear_interpolation_tests, ('test',))+ \
            map(cubic_spline_interpolation_tests, ('test_list', 'test_array'))
    unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# linear algebra test suite
#

class solve_tridiagonal_system_tests(unittest.TestCase):
  def test(self):

    # Solve,
    #  x +  y = 3
    #  y +  z = 5
    #  y + 2z = 8
    #
    # This implies,
    # 
    # A = 3x3
    #     [   1    1    0   
    #         0    1    1
    #         0    1    2 ]
    #
    # and r = [ 3, 5, 8 ]'.

    a = [None, 0, 1]
    b = [1, 1, 2]
    c = [1, 1, None]
    r = [3, 5, 8]

    # Expected result is x =[ 1 2 3 ]'.
      
    x = ppf.math.solve_tridiagonal_system(3, a, b, c, r)
    assert len(x) == 3 and x[0] == 1 and x[1] == 2

class solve_upper_diagonal_system_tests(unittest.TestCase):
  def test(self):
    
    # Solve upper diagonal system of linear equations ax = b
    # where
    #
    # a = 3x3
    #     [  1.75    1.5    -2.5
    #         0     -0.5    0.65
    #         0        0    0.25 ]
    #
    # and b = [0.5, -1.0, 3.5].
  

    a = ppf.math.array2d([3,3])
    a[0, 0], a[0, 1], a[0, 2] = (1.75, 1.5, -2.5)
    a[1, 0], a[1, 1], a[1, 2] = (0.0, -0.5,  0.65)
    a[2, 0], a[2, 1], a[2, 2] = (0.0,  0.0,  0.25)

    b = ppf.math.array1d([3])
    b[0] =  0.5
    b[1] = -1.0
    b[2] =  3.5
    #a = numpy.array([[1.75, 1.5, -2.5],
    #                 [0.0, -0.5,  0.65],
    #                 [0.0,  0.0,  0.25]])
    #b = numpy.array([0.5, -1.0, 3.5])

    # Expected solution vector is x = [2.97142857  20.2  14.0]'.
  
    x = ppf.math.solve_upper_diagonal_system(a, b)
    assert len(x) == 3 and math.fabs(x[0] - 2.971428571) < 1.0e-6 \
           and math.fabs(x[1] - 20.2) < 1.0e-6 and math.fabs(x[2] - 14.0) < 1.0e-6

class singular_value_decomposition_back_substitution_tests(unittest.TestCase):
  def test(self):
    
    # Solve upper diagonal system of linear equations ax = b using svd
    # where
    #
    # a = 3x3
    #     [  1.75    1.5    -2.5
    #         0     -0.5    0.65
    #         0        0    0.25 ]
    #
    # and b = [0.5, -1.0, 3.5].
  

    a = numpy.array([[1.75, 1.5, -2.5],
                     [0.0, -0.5,  0.65],
                     [0.0,  0.0,  0.25]])
    b = numpy.array([0.5, -1.0, 3.5])

    # Expected solution vector is x = [2.97142857  20.2  14.0]'.
  
    u, w, v = numpy.linalg.svd(a)
    x = ppf.math.singular_value_decomposition_back_substitution(u, w, v, b)
    assert len(x) == 3 and math.fabs(x[0] - 2.971428571) < 1.0e-6 \
           and math.fabs(x[1] - 20.2) < 1.0e-6 and math.fabs(x[2] - 14.0) < 1.0e-6

    
class linear_algebra_test_suite(unittest.TestSuite):
    def __init__(self):
       tests = map(solve_tridiagonal_system_tests, ('test',)) +\
               map(solve_upper_diagonal_system_tests, ('test',)) +\
               map(singular_value_decomposition_back_substitution_tests, ('test',))

       unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# generalised least squares test suite
#

class linear_fo:
  def __call__(self, x):
    return x[0]
class quadratic_fo:
  def __call__(self, x):
    return x[0]*x[0]

class generalised_least_squares_fit_tests(unittest.TestCase):
  def test(self):
    generator = random.Random(1234)
    ndata = 100
    sig = numpy.zeros(ndata)
    sig.fill(1.0)
    y = numpy.zeros(ndata)
    x = numpy.zeros([ndata, 1])
    a = 0.25
    b = -0.1
    for i in range(ndata):
      v = generator.gauss(0.0, 1.0)
      x[i, 0] = v
      y[i] = a*v+b*v*v
    fit_fos = []
    fit_fos.append(linear_fo())
    fit_fos.append(quadratic_fo())
    coeffs = ppf.math.generalised_least_squares_fit(y, x, sig, fit_fos)
    assert math.fabs(coeffs[0]-0.25) < 1.0e-6
    assert math.fabs(coeffs[1]+0.1) < 1.0e-6

class generalised_least_squares_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(generalised_least_squares_fit_tests, ('test',))
    unittest.TestSuite.__init__(self, tests) 

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# root finding test suite
#

class bisect_tests(unittest.TestCase):
  def test1(self):
    tol = 5*ppf.math.epsilon()
    left, right, num_its = \
          ppf.math.bisect(lambda x: x*x + 2.0*x - 1.0
                         , -3, -2
                         , lambda x, y: math.fabs(x-y) < tol, 100)
    assert num_its < 100
    assert math.fabs((left + right)/2 - (-1 - math.sqrt(2.))) < tol

  def test2(self):
    tol = 5*ppf.math.epsilon()
    left, right, num_its = \
          ppf.math.bisect(lambda x: x*x + 2.0*x - 1.0
                         , 0, 1
                         , lambda x, y: math.fabs(x-y) < tol, 100)
    assert num_its < 100
    assert math.fabs((left + right)/2 - (-1 + math.sqrt(2.))) < tol

class newton_raphson_tests(unittest.TestCase):
  def test(self):
    tol = 5*ppf.math.epsilon()
    guess, l, u, bin_digits = -3.0, -3.0, -2.0, 22
    root, its = \
         ppf.math.newton_raphson( \
           lambda x: (x*x + 2.0*x - 1.0, 2.0*x + 2.0)
           , guess, l, u, bin_digits, 100)
    assert its < 100
    assert math.fabs(root - (-1 - math.sqrt(2.))) < tol

class root_finding_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(bisect_tests, ('test1','test2')) + \
            map(newton_raphson_tests, ('test',))
    unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# piecewise cubic fitting test suite
#

class piecewise_cubic_fitting_tests(unittest.TestCase):
  def test(self):
    x = numpy.linspace(-1.5, 1.5, 7)
    y = numpy.zeros(7)
    for i in range(0, 7):
      y[i] = 1.5+0.5*x[i]+0.25*x[i]*x[i]-2.25*x[i]*x[i]*x[i]
    c = ppf.math.piecewise_cubic_fit(x, y)
    assert len(c.shape) == 2 and c.shape[0] == 4 and c.shape[1] == 3
    for i in range(0, 3):
      assert math.fabs(c[0][i] - 1.5) < 1.0e-6
    for i in range(0, 3):
      assert math.fabs(c[1][i] - 0.5) < 1.0e-6
    for i in range(0, 3):
      assert math.fabs(c[2][i] - 0.25) < 1.0e-6
    for i in range(0, 3):
      assert math.fabs(c[3][i] - -2.25) < 1.0e-6

class polynomial_fitting_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(piecewise_cubic_fitting_tests, ('test',))
    unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# normal distribution integral test suite
#

class normal_distribution_integral_tests(unittest.TestCase):
  def test1(self):
    mean = 0.05
    vol = 0.1
    f = ppf.math.normal_distribution(mean, vol)
    cs = [1.0]
    assert f.integral(cs, -10000, 10000) == 1.0
    cs = [0.0,1.0]
    assert f.integral(cs, -10000, 10000) == 0.05
    cs = [0.0,0.0,1.0]
    assert math.fabs(f.integral(cs, -10000, 10000) - 0.0125) < 1.0e-6

  def test2(self):
    mean = 0.05
    vol = 0.1
    f = ppf.math.normal_distribution(mean, vol)
    yls = f.moments(4, -1)
    yhs = f.moments(4, 10000)
    cs = [0.0,0.0,1.0,1.0]
    assert math.fabs(f.integral_max(cs, -10000, 10000) \
                     - 0.014125) < 1.0e-6
    assert math.fabs(cs[2]*(yhs[2]-yls[2])+cs[3]*(yhs[3]-yls[3]) \
                     - 0.014125) < 1.0e-6


class normal_distribution_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(normal_distribution_integral_tests, ('test1','test2'))
    unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# integrator test suite
#

class integrator_tests(unittest.TestCase):
  def lognormal_martingale_test(self):
    integrator = ppf.math.semi_analytic_domain_integrator()
    nt = 31
    nT = 31
    ntT = 31
    t = 0.5
    T = 1.0
    mut = 0.0
    muT = 0.0
    vol = 0.2
    volt = vol*math.sqrt(t)
    volT = vol*math.sqrt(T)
    ft = ppf.math.normal_distribution(mut, volt)
    fT = ppf.math.normal_distribution(muT, volT)
    xt = ft.state(5.5, nt)
    xT = fT.state(5.5, nT)
    meantT = muT-mut
    voltT = math.sqrt(volT*volT-volt*volt)
    ftT = ppf.math.normal_distribution(meantT, voltT)
    xtT = ftT.state(5.5, ntT)
    yT = numpy.zeros(nT)
    for i in range(nT): 
      yT[i] = math.exp(xT[i]-0.5*volT*volT) # lognormal martingale
    yt = integrator.rollback(t, T, xt, xT, xtT, ftT, yT)
    assert math.fabs(yt[15] - 0.990050) < 1.0e-6

  def tower_law_test(self):
    integrator = ppf.math.semi_analytic_domain_integrator()
    nt = 31
    nT = 31
    ntT = 31
    t = 0.5
    T = 1.0
    mut = 0.0
    muT = 0.0
    vol = 0.2
    volt = vol*math.sqrt(t)
    volT = vol*math.sqrt(T)
    ft = ppf.math.normal_distribution(mut, volt)
    fT = ppf.math.normal_distribution(muT, volT)
    xt = ft.state(5.5, nt)
    xT = fT.state(5.5, nT)
    meantT = muT-mut
    voltT = math.sqrt(volT*volT-volt*volt)
    ftT = ppf.math.normal_distribution(meantT, voltT)
    xtT = ftT.state(5.5, ntT)
    yT = numpy.zeros(nT)
    for i in range(nT): 
      yT[i] = math.exp(xT[i]-0.5*volT*volT) # lognormal martingale
    yt = integrator.rollback(t, T, xt, xT, xtT, ftT, yT)
    ns = 31
    s = 0
    mus = 0.0
    vols = 0.0
    fs = ppf.math.normal_distribution(mus, vols)
    xs = fs.state(5.5, ns)
    meansT = muT-mus
    volsT = math.sqrt(volT*volT-vols*vols)
    fsT = ppf.math.normal_distribution(meansT, volsT)
    xsT = fsT.state(5.5, ntT)
    ys = integrator.rollback(s, T, xs, xT, xsT, fsT, yT)
    meanst = mut-mus
    volst = math.sqrt(volt*volt-vols*vols)
    fst = ppf.math.normal_distribution(meanst, volst)
    xst = fst.state(5.5, ntT)
    ys1 = integrator.rollback(s, t, xs, xt, xst, fst, yt)
    for i in range(ns):
      assert math.fabs(ys[i]-ys1[i]) < 1.0e-6

  def atm_option_test(self):
    integrator = ppf.math.semi_analytic_domain_integrator()
    nT = 31
    t = 0.5
    T = 1.0
    mut = 0.0
    muT = 0.0
    vol = 0.2
    volt = vol*math.sqrt(t)
    volT = vol*math.sqrt(T)
    fT = ppf.math.normal_distribution(muT, volT)
    xT = fT.state(5.5, nT)
    yT = numpy.zeros(nT)
    for i in range(nT): 
      yT[i] = math.exp(xT[i]-0.5*volT*volT) # lognormal martingale
    ns = 31
    nsT = 31
    s = 0
    mus = 0.0
    vols = 0.0
    fs = ppf.math.normal_distribution(mus, vols)
    xs = fs.state(5.5, ns)
    meansT = muT-mus
    volsT = math.sqrt(volT*volT-vols*vols)
    fsT = ppf.math.normal_distribution(meansT, volsT)
    xsT = fsT.state(5.5, nsT)
    for i in range(nT): 
      yT[i] -= 1.0 # strike 1.0
    ys = integrator.rollback_max(s, T, xs, xT, xsT, fsT, yT)
    d1 = 0.5*volT
    for i in range(ns): 
      assert math.fabs(ys[i] - (2.0*fsT.unit_cdf(d1)-1.0)) < 1.0e-4

class integrator_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(integrator_tests, ('lognormal_martingale_test','tower_law_test'\
                                  ,'atm_option_test'))
    unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# driver
#

def suite():
  all_tests = unittest.TestSuite(
      (
        interpolation_test_suite()
      , linear_algebra_test_suite()
      , generalised_least_squares_test_suite()
      , root_finding_test_suite()
      , polynomial_fitting_test_suite()
      , normal_distribution_test_suite()
      , integrator_test_suite()
      ) )

  return all_tests
       
def run_tests():
  runner = unittest.TextTestRunner()
  runner.run(suite())

if __name__ == '__main__':  run_tests()
