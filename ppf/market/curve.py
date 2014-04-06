class curve(object):
  '''
  >>> import math
  >>> from ppf.math.interpolation import loglinear
  >>> times = range(0, 22)
  >>> factors = [math.exp(-0.05*T) for T in times]
  >>> P = curve(times, factors, loglinear)
  >>> for t in times: print P(t)
  1.0
  0.951229424501
  0.904837418036
  0.860707976425
  0.818730753078
  0.778800783071
  0.740818220682
  0.704688089719
  0.670320046036
  0.637628151622
  0.606530659713
  0.57694981038
  0.548811636094
  0.522045776761
  0.496585303791
  0.472366552741
  0.449328964117
  0.427414931949
  0.406569659741
  0.386741023455
  0.367879441171
  0.349937749111

  '''
  def __init__(self, times, factors, interp):
    self.__impl = interp(times, factors)
  def __call__(self, t): return self.__impl(t)

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
