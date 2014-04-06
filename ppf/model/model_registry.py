class model_registry:
   '''
   >>> registry = model_registry()
   >>> registry.add("model 1", "model 1 factory")
   >>> print registry
   {'model 1': 'model 1 factory'}
   '''
   registry = {}
   def add(self, name, factory):
     model_registry.registry[name] = factory

   def remove(self, name):
     if model_registry.registry.has_key(name):
       model_registry.registry.pop(name)
   
   def __str__(self):
     return model_registry.registry.__str__()

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
  _test()
