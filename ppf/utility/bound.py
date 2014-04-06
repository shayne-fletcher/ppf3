import operator

def lower_bound(x, values, cmp=operator.lt):
  """Find the first position in values
  where x could be inserted without violating
  the ordering.

  >>> values = [1, 2, 3]
  >>> print lower_bound(0, values)
  0
  >>> print lower_bound(1, values)
  0
  >>> print lower_bound(1.5, values)
  1
  >>> print lower_bound(3.1, values)
  3

  """
  first, count = 0, len(values)
  while count > 0:
    half = count/2
    middle = first + half
    if cmp(values[middle], x):
          first = middle + 1
          count = count - half - 1
    else: count = half

  return first

def upper_bound(x, values, cmp=operator.lt):
  """Find the last position in values
  where x could be inserted without changing
  the ordering.

  >>> values = [1, 2, 3, 3]
  >>> print upper_bound(0, values)
  0
  >>> print upper_bound(3, values)
  4
  >>> print upper_bound(4, values)
  4
  
  """
  first, count = 0, len(values)
  while count > 0:
    half = count/2
    middle = first + half
    if cmp(x, values[middle]):
      count = half
    else:
      first = middle + 1
      count = count - half - 1

  return first

def equal_range(x, values, cmp=operator.lt):
  """Find the largest subrange in which
    x could be inserted in any place without
    changing the ordering.

  >>> values = [1, 2, 3, 3, 4]
  >>> print equal_range(1.4, values)
  (1, 1)
  >>> print equal_range(3, values)
  (2, 4)

  """
  return (lower_bound(x, values, cmp), upper_bound(x, values, cmp))

def bound(x, values, cmp=operator.lt):
  """Raise if x is outside of the domain
  else find indices, i, j such that values[i] <= x <= values[j].

  >>> values = [1, 2, 3]
  >>> i, j = bound(1.5, values)
  >>> values[i] <= 1.5 <= values[j]
  True

  >>> i, j = bound(2, values)
  >>> values[i] <= 2 <= values[j]
  True

  >>> i, j = bound(4, values)
  Traceback (most recent call last):
    File "<stdin>", line 1, in ?
    File "interpolation.py", line 102, in bound
      raise RuntimeError, "%f lies right of the domain" % x
  RuntimeError: 4.000000 lies right of the domain
  >>> i, j = bound(0, values)
  Traceback (most recent call last):
    File "c:\Python24\lib\doctest.py", line 1243, in __run
      compileflags, 1) in test.globs
    File "<doctest __main__.bound[12]>", line 1, in ?
      i, j = bound(0, values)
    File "interpolation.py", line 113, in bound
      raise RuntimeError, "%f lies left of the domain" % x
  RuntimeError: 0.000000 lies left of the domain

  """
  count = len(values)
  left, right = equal_range(x, values, cmp)
  if left == count:
    raise RuntimeError ("%f lies right of the domain" % x)
  elif right == 0:
    raise RuntimeError ("%f lies left of the domain" % x)

  if right == count: right -= 1
  if left == right:   left -= 1

  return (left, right)

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()
