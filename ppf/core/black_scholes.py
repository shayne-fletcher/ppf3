from math import log, sqrt, exp
from ppf.math import N

def black_scholes(S, K, r, sig, T, CP, *arguments, **keywords):
  """The classic Black and Scholes formula.

  >>> print black_scholes(S=42., K=40., r=0.1, sig= 0.2, T=0.5, CP=CALL)
  4.75942193531

  >>> print black_scholes(S=42., K=40., r=0.1, sig= 0.2, T=0.5, CP=PUT)
  0.808598915338

  """
  if K <= 0:
    raise RuntimeError ("strike must be non-negative")
  if sig <= 0:
    raise RuntimeError ("vol must be non-negative")
  if T <= 0:
    raise RuntimeError ("time to maturity must be non-negative")

  d1 = (log(S/K) + (r + 0.5*(sig*sig))*T)/(sig*sqrt(T))
  d2 = d1 - sig*sqrt(T)

  return CP*S*N(CP*d1) - CP*K*exp(-r*T)*N(CP*d2)

CALL, PUT = (1, -1)

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()
