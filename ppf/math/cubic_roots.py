import math
from .quadratic_roots import *

def cubic_roots(a, b, c, d, xl, xh):
  if a != 0:
    roots = []
    aa = a
    a = b/aa
    b = c/aa
    c = d/aa
    q = (a*a-3*b)/9.0
    r = (2*a*a*a-9.0*a*b+27.0*c)/54.0
    q3 = q*q*q
    diff = r*r-q3
    if diff <= 0:
      ratio = r/math.sqrt(q3)
      theta = math.acos(ratio)
      qr = -2.0*math.sqrt(q)
      a_over_3 = a/3.0
      r1 = qr*math.cos(theta/3.0)-a_over_3
      r2 = qr*math.cos((theta+2.0*math.pi)/3.0)-a_over_3
      r3 = qr*math.cos((theta-2.0*math.pi)/3.0)-a_over_3
      rs = [r1, r2, r3]
      rs.sort()
      [r1, r2, r3] = rs
      if r1 >= xl and r1 <= xh:
        roots.append(r1)
      if r2 != r1 and r2 >= xl and r2 <= xh:
        roots.append(r2) 
      if r3 != r1 and r3 != r2 and r3 >= xl and r3 <= xh:
        roots.append(r3) 
    else:
      biga = 0  
      if r > 0:
        biga = -math.pow(r+math.sqrt(diff), 1.0/3.0)
      else:
        biga = math.pow(-r+math.sqrt(diff), 1.0/3.0)
      bigb = 0.0
      if biga != 0: bigb = q/biga
      r1 = (biga+bigb)-a/3.0
      if r1 >= xl and r1 <= xh:
        roots.append(r1)
    return roots
  else:
    return quadratic_roots(b, c, d, xl, xh)
