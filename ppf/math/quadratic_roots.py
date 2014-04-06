import math
def quadratic_roots(a, b, c, xl, xh):
  # find roots
  roots = []
  d = b*b-4*a*c
  if d > 0:
    r1 = 0
    r2 = 0
    if a != 0:
      sgn = 1
      if b < 0: sgn = -1
      q = -0.5*(b+sgn*math.sqrt(d))
      r1 = q/a
      r2 = r1
      if q != 0: r2 = c/q
    else:
      r1 = -c/b
      r2 = r1
    # order roots
    if r1 > r2:
      tmp = r1
      r1 = r2
      r2 = tmp
    if r1 >= xl and r1 <= xh:
      roots.append(r1)
    if r2 != r1 and r2 >= xl and r2 <= xh:
      roots.append(r2)
  else:
    if a != 0:
      r1 = -b/(2*a)
      if r1 >= xl and r1 <= xh:
        roots.append(r1)

  return roots
