import ppf, math, numpy, unittest

def _assert_seq_close(a, b, tol=1.0e-8):
  assert (len(a) == len(b)) and \
  not [l for l in [math.fabs(x - y) <= tol for (x, y) in zip(a, b)] if not l]

class requestor_tests(unittest.TestCase):
  def test_discount_factor(self):
    env = ppf.market.environment()
    times = numpy.linspace(0, 2, 5)
    env.add_curve(
          "zc.disc.eur"
        , ppf.market.curve(
              times
            , numpy.array([math.exp(-0.05*t) for t in times])
            , ppf.math.interpolation.loglinear
              )
          )
    r = ppf.model.hull_white.requestor()
    t = 1.5
    Bt = [r.discount_factor(t, "eur", env)]

    _assert_seq_close([0.927743486329], Bt)

  def test_term_vol(self):
    env = ppf.market.environment()
    env.add_constant("cv.mr.eur.hw", 0.0)
    expiries, tenors = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0], [0, 90]
    env.add_surface(
        "ve.term.eur.hw"
      , ppf.market.surface(expiries, tenors, numpy.array(8*[[0.04, 0.04]]))
      )
    r = ppf.model.hull_white.requestor()
    t = 0.25
    sig = [r.term_vol(t, "eur", env)]

    _assert_seq_close(sig, [0.1])

class state_tests(unittest.TestCase):
  def test(self):
    expiries, tenors = [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0], [0, 90]
    surf = ppf.market.surface(expiries, tenors, numpy.array(8*[[0.04, 0.04]]))
    env = ppf.market.environment()
    env.add_surface("ve.term.eur.hw", surf)
    env.add_constant(  "cv.mr.eur.hw", 0.01)
    s =  ppf.model.hull_white.lattice.state("eur", 11, 3.5)
    x = s.fill(1.25, ppf.model.hull_white.requestor(), env)
    exp = \
      [-0.78754076
      ,-0.63003261
      ,-0.47252446
      ,-0.31501631
      ,-0.15750815
      , 0.
      , 0.15750815
      , 0.31501631
      , 0.47252446
      , 0.63003261
      , 0.78754076]

    _assert_seq_close(exp, x)

class fill_tests(unittest.TestCase):
  def test_numeraire_rebased_bond(self):
    env = ppf.market.environment()
    times = numpy.linspace(0, 2, 5)
    factors = numpy.array([math.exp(-0.05*t) for t in times])
    env.add_curve("zc.disc.eur"
        , ppf.market.curve(times, factors, ppf.math.interpolation.loglinear))
    expiries, tenors =      [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0], [0, 90]
    env.add_surface("ve.term.eur.hw"
                 , ppf.market.surface(expiries, tenors, numpy.zeros((8, 2))))
    env.add_constant("cv.mr.eur.hw", 0.0)
    r = ppf.model.hull_white.requestor()
    s = ppf.model.hull_white.lattice.state("eur", 11, 3.5)
    sx = s.fill(0.25, r, env)
    f = ppf.model.hull_white.fill(2.0)
    PtT = f.numeraire_rebased_bond(0.25, 1.5, "eur", env, r, sx)
    exp = \
        [0.927743486329
        ,0.927743486329
        ,0.927743486329
        ,0.927743486329
        ,0.927743486329
        ,0.927743486329
        ,0.927743486329
        ,0.927743486329
        ,0.927743486329
        ,0.927743486329
        ,0.927743486329]

    _assert_seq_close(exp, PtT)

  def test_libor(self):
    from ppf.date_time \
         import date, shift, modified_following, basis_act_360, months
    pd = date(2008, 01, 01)
    env = ppf.market.environment(pd)
    times = numpy.linspace(0, 2, 5)
    factors = numpy.array([math.exp(-0.05*t) for t in times])
    env.add_curve("zc.disc.eur"
        , ppf.market.curve(times, factors, ppf.math.interpolation.loglinear))
    expiries, tenors =      [0.1, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0], [0, 90]
    env.add_surface("ve.term.eur.hw"
                 , ppf.market.surface(expiries, tenors, numpy.zeros((8, 2))))
    env.add_constant("cv.mr.eur.hw", 0.0)
    rd = date(2008, 07, 01)
    libor_obs = \
      ppf.core.libor_rate( \
           None #attributes
         , 0    #flow-id
         , 0    #reset-id
         , rd   #reset-date
         , "eur"#reset-currency
         , rd   #projection-start-date
         , shift(rd + months(6), modified_following)#projection-end-date
         , basis_act_360#projection-basis
         , ppf.core.fixing(False))# fixing (and no spread)
    r = ppf.model.hull_white.requestor()
    s = ppf.model.hull_white.lattice.state("eur", 11, 3.5)
    sx = s.fill(0.25, r, env)
    f = ppf.model.hull_white.fill(2.0)
    libortT = f.libor(0.25, libor_obs, env, r, sx)
    exp = \
        [0.0499418283138
        ,0.0499418283138
        ,0.0499418283138
        ,0.0499418283138
        ,0.0499418283138
        ,0.0499418283138
        ,0.0499418283138
        ,0.0499418283138
        ,0.0499418283138
        ,0.0499418283138
        ,0.0499418283138
         ]

    _assert_seq_close(exp, libortT)

class rollback_tests(unittest.TestCase):
  def test_discounted_libor_rollback(self):
    from ppf.date_time \
         import date, shift, modified_following, basis_act_360, months
    pd = date(2008, 01, 01)
    env = ppf.market.environment(pd)
    times = numpy.linspace(0, 6, 10)
    factors = numpy.array([math.exp(-0.05*t) for t in times])
    env.add_curve("zc.disc.eur"
        , ppf.market.curve(times, factors, ppf.math.interpolation.loglinear))
    expiries, tenors = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0], [0, 90]
    values = numpy.zeros((9, 2))
    values.fill(0.001)
    env.add_surface("ve.term.eur.hw"
                 , ppf.market.surface(expiries, tenors, values))
    env.add_constant("cv.mr.eur.hw", 0.01)
    r = ppf.model.hull_white.requestor()
    s = ppf.model.hull_white.lattice.state("eur", 41, 4.5)
    f = ppf.model.hull_white.fill(5.0)
    rd = date(2011, 01, 01)
    libor_obs = \
      ppf.core.libor_rate( \
           None #attributes
         , 0    #flow-id
         , 0    #reset-id
         , rd   #reset-date
         , "eur"#reset-currency
         , rd   #projection-start-date
         , shift(rd + months(6), modified_following)#projection-end-date
         , basis_act_360#projection-basis
         , ppf.core.fixing(False))# fixing (and no spread)
    t = env.relative_date(libor_obs.proj_start_date())/365.0
    T = env.relative_date(libor_obs.proj_end_date())/365.0
    sx = s.fill(t, r, env)
    libort = f.libor(t, libor_obs, env, r, sx)
    ptT = f.numeraire_rebased_bond(t, T, "eur", env, r, sx)
    pv = libort*ptT*libor_obs.year_fraction()
    roll = ppf.model.hull_white.lattice.rollback("eur")
    intermediate_pv = roll.rollback(0.5*t, t, s, r, env, pv)
    actual = roll.rollback(0.0, 0.5*t, s, r, env, intermediate_pv).mean() 
    expected = r.discount_factor(t, "eur", env)-r.discount_factor(T, "eur", env)
    _assert_seq_close([expected],[actual],1.0e-6)

  def test_bond_option(self):    
    from ppf.date_time \
         import date, shift, modified_following, basis_act_360, months
    pd = date(2008, 01, 01)
    env = ppf.market.environment(pd)
    times = numpy.linspace(0, 6, 10)
    factors = numpy.array([math.exp(-0.05*t) for t in times])
    env.add_curve("zc.disc.eur"
        , ppf.market.curve(times, factors, ppf.math.interpolation.loglinear))
    expiries, tenors = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0], [0, 90]
    values = numpy.zeros((9, 2))
    values.fill(0.001)
    env.add_surface("ve.term.eur.hw"
                 , ppf.market.surface(expiries, tenors, values))
    env.add_constant("cv.mr.eur.hw", 0.01)
    r = ppf.model.hull_white.requestor()
    s = ppf.model.hull_white.lattice.state("eur", 41, 4.5)
    f = ppf.model.hull_white.fill(5.0)
    t = 3.0
    T = 4.0
    terminal_T = 5.0
    sx = s.fill(t, r, env)
    ptT = f.numeraire_rebased_bond(t, T, "eur", env, r, sx)
    k = 0.9
    pv = ptT-k
    roll = ppf.model.hull_white.lattice.rollback("eur")    
    actual = roll.rollback_max(0.0, t, s, r, env, pv).mean()
    volt = r.term_vol(t, "eur", env)*r.local_vol(T, terminal_T, "eur", env)
    F = r.discount_factor(T, "eur", env)
    d1 = math.log(F/k)/volt+0.5*volt
    d2 = d1-volt
    expected = F*ppf.math.N(d1)-k*ppf.math.N(d2)
    _assert_seq_close([expected],[actual],1.0e-5)

  def test_constant(self):
    from ppf.date_time \
         import date, shift, modified_following, basis_act_360, months
    pd = date(2008, 01, 01)
    env = ppf.market.environment(pd)
    times = numpy.linspace(0, 6, 10)
    factors = numpy.array([math.exp(-0.05*t) for t in times])
    env.add_curve("zc.disc.eur"
        , ppf.market.curve(times, factors, ppf.math.interpolation.loglinear))
    expiries, tenors = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0], [0, 90]
    values = numpy.zeros((9, 2))
    values.fill(0.001)
    env.add_surface("ve.term.eur.hw"
                 , ppf.market.surface(expiries, tenors, values))
    env.add_constant("cv.mr.eur.hw", 0.01)
    r = ppf.model.hull_white.requestor()
    s = ppf.model.hull_white.lattice.state("eur", 41, 5.5)
    f = ppf.model.hull_white.fill(5.0)
    t = 3.0
    T = 4.0
    terminal_T = 5.0
    sx = s.fill(t, r, env)
    yT = numpy.zeros(41)
    yT.fill(1)
    roll = ppf.model.hull_white.lattice.rollback("eur")    
    yt = roll.rollback(t, T, s, r, env, yT)
    _assert_seq_close(yt, yT, 1.0e-5)

class evolve_tests(unittest.TestCase):
  def test_mean_and_variance(self):
    from ppf.date_time \
         import date, shift, modified_following, basis_act_360, months
    pd = date(2008, 01, 01)
    env = ppf.market.environment(pd)
    times = numpy.linspace(0, 6, 10)
    factors = numpy.array([math.exp(-0.05*t) for t in times])
    env.add_curve("zc.disc.eur"
        , ppf.market.curve(times, factors, ppf.math.interpolation.loglinear))
    expiries, tenors = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0], [0, 90]
    values = numpy.zeros((9, 2))
    values.fill(0.001)
    env.add_surface("ve.term.eur.hw"
                 , ppf.market.surface(expiries, tenors, values))
    env.add_constant("cv.mr.eur.hw", 0.01)
    r = ppf.model.hull_white.requestor()
    s = ppf.model.hull_white.monte_carlo.state(10000)
    e = ppf.model.hull_white.monte_carlo.evolve("eur")
    e.evolve(0.0,0.5,s,r,env)
    e.evolve(0.5,1.0,s,r,env)
    variates = s.get_variates()
    mean = variates.sum()/10000
    assert(math.fabs(mean) < 1.0e-4)
    tmp = variates*variates
    variance = tmp.sum()/10000
    vol = r.term_vol(1.0,"eur",env)
    assert(math.fabs(variance-vol*vol) < 1.0e-4)

  def test_bond(self):
    from ppf.date_time \
         import date, shift, modified_following, basis_act_360, months
    pd = date(2008, 01, 01)
    env = ppf.market.environment(pd)
    times = numpy.linspace(0, 6, 10)
    factors = numpy.array([math.exp(-0.05*t) for t in times])
    env.add_curve("zc.disc.eur"
        , ppf.market.curve(times, factors, ppf.math.interpolation.loglinear))
    expiries, tenors = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0], [0, 90]
    values = numpy.zeros((9, 2))
    values.fill(0.001)
    env.add_surface("ve.term.eur.hw"
                 , ppf.market.surface(expiries, tenors, values))
    env.add_constant("cv.mr.eur.hw", 0.01)
    r = ppf.model.hull_white.requestor()
    s = ppf.model.hull_white.monte_carlo.state(10000)
    e = ppf.model.hull_white.monte_carlo.evolve("eur")
    e.evolve(0.0,3.0,s,r,env)
    f = ppf.model.hull_white.fill(5.0)
    t = 3.0
    T = 4.0
    sx = s.fill(t, r, env)
    ptT = f.numeraire_rebased_bond(t, T, "eur", env, r, sx)
    actual = ptT.mean()
    expected = r.discount_factor(T, "eur", env)
    assert(math.fabs(actual-expected) < 1.0e-3)

class exercise_tests(unittest.TestCase):
  def test_explanatory_variables(self):
    from ppf.math.interpolation import loglinear
    times = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    factors = [math.exp(-0.05*t) for t in times]
    c = ppf.market.curve(times, factors, loglinear)
    expiries = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
    tenors = [0, 90]
    values = numpy.zeros((8, 2))
    surf = ppf.market.surface(expiries, tenors, values)
    from ppf.date_time \
         import date, shift_convention, modified_following, basis_act_360, months
    pd = date(2008, 01, 01)
    env = ppf.market.environment(pd)
    key = "zc.disc.eur"
    env.add_curve(key, c)
    key = "ve.term.eur.hw"
    env.add_surface(key, surf)
    key = "cv.mr.eur.hw"
    env.add_constant(key, 0.0)
    r = ppf.model.hull_white.requestor()
    s = ppf.model.hull_white.monte_carlo.state(10)
    sx = s.fill(0.25, r, env)
    f = ppf.model.hull_white.fill(3.0)
    flows = ppf.core.generate_flows(
             start  = date(2008, 01, 01)
            , end  = date(2010, 01, 01)
            , duration = months
            , period = 6
            , shift_method = shift_convention.modified_following
            , basis = "ACT/360"
            , pay_currency = "EUR")
    lg = ppf.core.leg(flows, ppf.core.PAY)
    ex = ppf.model.hull_white.monte_carlo.cle_exercise(lg)
    t = env.relative_date(flows[1].accrual_start_date())/365.0
    T = env.relative_date(flows[1].accrual_end_date())/365.0
    ret = ex(t, f, sx, r, env)
    dft = c(t)
    dfT = c(T)
    expected_libor = (dft/dfT-1.0)/flows[1].year_fraction()
    pv01 = 0.0
    for fl in flows[1:]:
      T = env.relative_date(fl.pay_date())/365.0
      dfT = c(T)
      pv01 += fl.year_fraction()*dfT
    T = env.relative_date(flows[-1].accrual_end_date())/365.0
    dfT = c(T)
    expected_swap = (dft-dfT)/pv01
    expected_libors = numpy.zeros(10)
    expected_libors.fill(expected_libor)
    expected_swaps = numpy.zeros(10)
    expected_swaps.fill(expected_swap)
    actual_libors = ret[:, 0]
    actual_swaps = ret[:, 1]

    _assert_seq_close(actual_libors, expected_libors)
    _assert_seq_close(actual_swaps, expected_swaps)

class hull_white_test_suite(unittest.TestSuite):
  def __init__(self):
    tests = map(requestor_tests,('test_discount_factor','test_term_vol')) + \
            map(state_tests,('test',))                                     + \
            map(fill_tests,('test_numeraire_rebased_bond', 'test_libor')) + \
            map(rollback_tests, ('test_discounted_libor_rollback','test_bond_option', 'test_constant')) + \
            map(evolve_tests, ('test_mean_and_variance', 'test_bond')) + \
            map(exercise_tests, ('test_explanatory_variables',))

    unittest.TestSuite.__init__(self, tests)

#////////1/////////2/////////3/////////4/////////5/////////6/////////7/////////8
# driver
#

def suite():
  all_tests = unittest.TestSuite(
      (
         hull_white_test_suite()
       , 
      ) )

  return all_tests
       
def run_tests():
  runner = unittest.TextTestRunner()
  runner.run(suite())

if __name__ == '__main__':  run_tests()
