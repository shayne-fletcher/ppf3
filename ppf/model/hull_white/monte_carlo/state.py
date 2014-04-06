import numpy

class state(object):
  def __init__(self, num_sims):
     self.__num_sims = num_sims
     self.__variates = numpy.zeros((num_sims))

  def num_sims(self):
     return self.__num_sims
  '''
  >>> s = state(10)
  >>> variates = numpy.zeros((10))
  >>> for i in range(10): variates[i] = 1
  >>> s.set_variates(variates)
  >>> for i in range(10): print s.get_variates()[i, 0]
  1.0
  1.0
  1.0
  1.0
  1.0
  1.0
  1.0
  1.0
  1.0
  1.0
  '''
  def fill(self, t, req, env):
     return self.__variates

  def set_variates(self, variates):
     if len(variates.shape) <> 1:
       raise RuntimeError, 'expected a 1d array of variates'
     if variates.shape[0] <> self.__num_sims:
       raise RuntimeError, 'mismatched number of simulations'
     self.__variates = variates
  
  def get_variates(self):
     return self.__variates

  def create_variable(self):
     var = numpy.zeros(self.__num_sims)
     return var  

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
