from .ppf_math import epsilon
from .ppf_math import min_flt
from .ppf_math import max_flt

import math

def sign(z):
  if z == 0: return 0
  elif z < 0 : return -1
  else: return 1

def N(x):
  a	  =  0.3535533905933
  b1  = -1.2655122300000
  b2  =  1.0000236800000
  b3  =  0.3740919600000
  b4  =  0.0967841800000
  b5  = -0.1862880600000
  b6  =  0.2788680700000
  b7  = -1.1352039800000
  b8  =  1.4885158700000
  b9  = -0.8221522300000
  b10 =  0.1708727700000

  t, term, result = 0, 0, 0
            
  if(x > 0):
    if (x > 10): result = 1.0
    else:
      t = 1/(1 + a*x)
      term = b9 + t*b10
      term = b8 + t*term
      term = b7 + t*term
      term = b6 + t*term
      term = b5 + t*term
      term = b4 + t*term
      term = b3 + t*term
      term = b2 + t*term
      term = b1 + t*term
      term = term + -0.5*(x*x) 

      result = 1.0 - 0.5*t*math.exp(term)
  else:
    if(x < -10): result = 0.0
    else:
      t = 1/(1 - a*x)
      term = b9 + t*b10
      term = b8 + t*term
      term = b7 + t*term
      term = b6 + t*term
      term = b5 + t*term
      term = b4 + t*term
      term = b3 + t*term
      term = b2 + t*term
      term = b1 + t*term
      term = term + -0.5*(x*x)
			
      result = 0.5*t*math.exp(term)
  
  return result
