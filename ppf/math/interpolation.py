import math
import ppf.utility
from . import linear_algebra

class interpolation_base(object):
  def __init__(self, abscissae, ordinates):
    if not sorted(abscissae) or \
         len(abscissae) != len(ordinates):
      raise RuntimeError ('abscissae/ordinates length mismatch')
    self.N = len(abscissae)
    self.abscissae, self.ordinates = abscissae, ordinates

  def locate(self, x):
    i, j = ppf.utility.bound(x, self.abscissae)
    x_lo, x_hi = self.abscissae[i], self.abscissae[j]
    y_lo, y_hi = self.ordinates[i], self.ordinates[j]

    return (i, j, x_lo, x_hi, y_lo, y_hi)
    
class linear(interpolation_base):
  def __init__(self, abscissae, ordinates):
    interpolation_base.__init__(self, abscissae, ordinates)

  def __call__(self, x):
    i, j, x_lo, x_hi, y_lo, y_hi = \
       interpolation_base.locate(self, x)
    R = 1.0 - (x_hi - x)/(x_hi - x_lo)

    return R*(y_hi - y_lo) + y_lo

class loglinear(interpolation_base):
  def __init__(self, abscissae, ordinates):
    interpolation_base.__init__(self, abscissae, ordinates)

  def __call__(self, x):
    i, j, x_lo, x_hi, y_lo, y_hi = \
       interpolation_base.locate(self, x)
    ln_ylo, ln_yhi = math.log(y_lo), math.log(y_hi)
    R = 1.0 - (x_hi - x)/(x_hi - x_lo)

    return math.exp(ln_ylo+(ln_yhi - ln_ylo)*R)

class linear_on_zero(interpolation_base):
  def __init__(self, abscissae, ordinates):
    interpolation_base.__init__(self, abscissae, ordinates)

  def __call__(self, x):
    x_0 = self.abscissae[0]
    i, j, x_lo, x_hi, y_lo, y_hi = \
       interpolation_base.locate(self, x)
    dx = (x_hi - x_lo)
    R, R_ = (1.0 - ((x_hi - x)/dx)), (x - x_0)/dx
    y = 0
    if i == 0:
      y = math.pow(y_hi, R_)
    else:
      r, r_lo, r_hi = x - x_0, x_lo - x_0, x_hi - x_0
      z_lo, z_hi = -math.log(y_lo)/r_lo, -math.log(y_hi)/r_hi
      y = math.exp(-(z_lo + R*(z_hi - z_lo))*r)

    return y

class linear_on_variance(interpolation_base):
  def __init__(self, abscissae, ordinates):
    interpolation_base.__init__(self, abscissae, ordinates)
  def __call__(self, x):
    i, j, x_lo, x_hi, y_lo, y_hi = \
       interpolation_base.locate(self, x)
    R = 1.0 - (x_hi - x)/(x_hi - x_lo)
    T, T_lo, T_hi = x/365.25, x_lo/365.25, x_hi/365.25
    Y_lo, Y_hi = y_lo*y_lo*T_lo, y_hi*y_hi*T_hi
    Y = R*(Y_hi - Y_lo) + Y_lo
    if Y < 0:
      raise RuntimeError ("Negative variance encountered")

    return math.sqrt(Y/T)

class cubic_spline(interpolation_base):
  def __init__(self, abscissae, ordinates, a_0 = 0.5, d_0=0, b_n=0.5, d_n=0):
    interpolation_base.__init__(self, abscissae, ordinates)
    xs, ys, N = self.abscissae, self.ordinates, self.N
    b = [d_0]+(N - 1)*[0]
    A_sub, A_dia, A_sup = N*[0], [2.0] + (N - 1)*[0], [a_0] + (N - 1)*[0]
    for i in range(1, N - 1):
      H, h = xs[i + 1]- xs[i], xs[i] -  xs[i - 1]
      b[i] = (6./(h + H))*(((ys[i + 1] - ys[i])/H) - ((ys[i] - ys[i - 1])/h))
      a_i = H/(h + H)
      b_i = 1.0 - a_i
      A_dia[i], A_sup[i], A_sub[i] = 2., a_i, b_i
    A_sub[N - 1], A_dia[N - 1], b[N - 1] = b_n, 2.0, d_n
    self.C = linear_algebra.solve_tridiagonal_system(N, A_sub, A_dia, A_sup, b)

  def __call__(self, x):
    xs, ys, C = self.abscissae, self.ordinates, self.C
    i, j, _, _, _, _ = interpolation_base.locate(self, x)
    h_i = xs[j] - xs[i]
    x_low = xs[j] - x
    x_low3 = math.pow(x_low, 3)
    x_high = x - xs[i]
    x_high3 = math.pow(x_high, 3)
    hi_sqrd_6 = h_i*h_i/6.0

    return  C[i]*x_low3/(6.0*h_i)+C[j]*x_high3/(6.0*h_i)+\
           (ys[i]-C[i]*hi_sqrd_6)*x_low/h_i+(ys[j]-C[j]*hi_sqrd_6)*x_high/h_i
