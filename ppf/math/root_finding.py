import math
from .special_functions import sign, max_flt

def bisect(f, min, max, tol, max_its):
  """Bisection method

  The quadratic y(x) = x^2 + 2x -1 has roots
  -1 - sqrt(2) = -2.4142135623730950488016887242097
  and -1 + sqrt(2) = 0.4142135623730950488016887242097.

  >>> bisect(lambda x: x*x + 2*x - 1, -3, -2, lambda x, y: math.fabs(x-y) < 0.000001, 10)
  (-2.4142141342163086, -2.4142131805419922, 3)

  >>> bisect(lambda x: x*x + 2*x - 1, 0, 1, lambda x, y: math.fabs(x-y) < 0.000001, 10)
  (0.41421318054199219, 0.41421413421630859, 3)

  """

  fmin, fmax = f(min), f(max)
  if fmin == 0: return (min, min, 0)
  if fmax == 0: return (max, max, 0)
  if min >= max: raise RuntimeError ("Arguments in wrong order")
  if fmin*fmax >= 0: raise RuntimeError ("Root not bracketed")

  count = max_its
  if count < 3:
    count = 0
  else: count -= 3

  while count and tol(min, max) == 0:
    mid = (min + max)/2.
    fmid = f(mid)
    if mid == max or mid ==min:
        break
    if fmid == 0:
      min = max = mid
      break
    elif sign(fmid)*sign(fmin) < 0:
      max, fmax = mid, fmid
    else:
      min, fmin = mid, fmid
    --count

  max_its -= count

  return (min, max, max_its)
 

def newton_raphson(f, guess, min, max, digits, max_its):
  """Newton-Raphson method

  The quadratic y(x) = x^2 + 2x -1 has roots
  -1 - sqrt(2) = -2.4142135623730950488016887242097
  and -1 + sqrt(2) = 0.4142135623730950488016887242097.
  
  >>> newton_raphson(lambda x: (x*x+2*x-1,2*x+2),-3,-3,-2,22,100)
  (-2.4142135623730949, 5)
  
  """

  def _handle_zero_derivative(f, last_f0, f0, delta, result, guess, min, max):
    if last_f0 == 0:
      # must be first iteration
      if result == min: guess = max
      else: guess = min
      last_f0, _ = f(guess)
      delta = guess - result
    if sign(last_f0)*sign(f0) < 0:
      # we've crossed over so move in opposite
      # direction to last step
      if delta < 0:
        delta = (result - min)/2.0
      else:
        delta = (result - max)/2.0
    else:
      # move in same direction of last step
      if delta < 0:
        delta = (result - max)/2.0
      else:
        delta = (result - min)/2.0
    return (last_f0, delta, result, guess)

  f0, f1, last_f0, result = 0.0, 0.0, 0.0, guess
  factor = math.ldexp(1.0, 1 - digits)
  delta, delta1, delta2 = 1.0, max_flt(), max_flt()
  count = max_its

  while True:
    last_f0 = f0
    delta2 = delta1
    delta1 = delta
    f0, f1 = f(result)
    if f0 == 0:
      break
    if f1 == 0:
      last_f0, delta, result, guess = \
               _handle_zero_derivative( \
                     f, last_f0, f0, delta, result, guess, min, max)
    else:
      delta = f0/f1

    if math.fabs(delta*2.0) > math.fabs(delta2):
      # last two steps haven't converged, try bisection
      delta = ((result - max)/2.0, (result - min)/2.0)[delta > 0]
    guess = result
    result -= delta
    if result <= min:
      delta = 0.5*(guess - min)
      result = guess - delta
      if result == min or result == max:
        break
    elif result >= max:
      delta = 0.5*(guess - max)
      result = guess - delta
      if result == min or result == max: break

    # update brackets
    if delta > 0:
      max = guess
    else:
      min = guess

    count -= 1

    if count != 0 and \
           math.fabs(result*factor) < math.fabs(delta):
      continue
    else:
      break

  max_its -= count

  return (result, max_its)
        
      
def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()

