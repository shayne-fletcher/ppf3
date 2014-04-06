class fixing(object):
  def __init__(self, is_fixed=False, value=None):
    self.__is_fixed = is_fixed
    self.__value = value
  def is_fixed(self): return self.__is_fixed
  def value(self): return self.__value
