import ppf.date_time

class environment(object):
  def __init__(self, pd = ppf.date_time.date(2008, 01, 01)):
    self.__pd = pd
    self.__curves = {}
    self.__surfaces = {}
    self.__constants = {}

  def pricing_date(self):
    return self.__pd

  def relative_date(self, d):
    ret = 0
    if isinstance(d, ppf.date_time.date):
      ret = ppf.date_time.days.days(d-self.__pd)
    else:
      ret = d-self.__pd.julian_day()
    if ret < 0:
      raise RuntimeError, 'date before pricing date'
    return ret
    
  def add_curve(self, key, curve):
    key = key.lower()    
    if self.__curves.has_key(key):
      del self.__curves[key]
    self.__curves[key] = curve 

  def add_surface(self, key, surface):
    key = key.lower()
    if self.__surfaces.has_key(key):
      del self.__surfaces[key]
    self.__surfaces[key] = surface

  def add_constant(self, key, constant):
    key = key.lower()
    if self.__constants.has_key(key):
      del self.__constants[key]
    self.__constants[key] = constant 

  def has_curve(self, key):
    key = key.lower()
    return self.__curves.has_key(key)

  def has_surface(self, key):
    key = key.lower()
    return self.__surfaces.has_key(key)

  def has_constant(self, key):
    key = key.lower()
    return self.__constants.has_key(key)

  def retrieve_curve(self, key):
    key = key.lower()
    if not self.has_curve(key):
      raise RuntimeError, 'unable to find curve "'+key+'"'
    return self.__curves[key]

  def retrieve_surface(self, key):
    key = key.lower()
    if not self.has_surface(key):
      raise RuntimeError, 'unable to find surface "'+key+'"'
    return self.__surfaces[key]

  def retrieve_constant(self, key):
    '''
    >>> env = environment()
    >>> key = 'test_key'
    >>> env.add_constant(key, 0.05)
    >>> print env.has_constant(key)
    1
    >>> value = env.retrieve_constant(key)
    >>> print value
    0.05
    '''
    key = key.lower()
    if not self.has_constant(key):
      raise RuntimeError, 'unable to find constant "'+key+'"'
    return self.__constants[key]

  def retrieve_keys(self):
    return self.__curves.keys()+self.__surfaces.keys()+self.__constants.keys()

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
 
