import ppf.utility

class surface(object):
  def __init__(self, first_axis, second_axis, values):
    self.__first_axis = first_axis
    self.__second_axis = second_axis
    self.__values = values

  def __call__(self, x, y):
    i1, i2 = ppf.utility.bound(x, self.__first_axis)
    j1, j2 = ppf.utility.bound(y, self.__second_axis)
    f = self.__values
    x1 = self.__first_axis[i1]
    x2 = self.__first_axis[i2]
    y1 = self.__second_axis[j1]
    y2 = self.__second_axis[j2]
    r = (x2 - x1)*(y2 - y1)
    return (f[i1, j1]/r)*(x2 - x)*(y2 - y) + \
           (f[i2, j1]/r)*(x - x1)*(y2 - y) + \
           (f[i1, j2]/r)*(x2 - x)*(y - y1) + \
           (f[i2, j2]/r)*(x - x1)*(y - y1)

