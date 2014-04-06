class model(object):
  def __init__(self, requestor, state, fill, rollback = None, evolve = None, exercise = None):
    self.__requestor = requestor
    self.__state = state
    self.__fill = fill
    self.__rollback = rollback
    self.__evolve = evolve
    self.__exercise = exercise
    # check that either the evolve or rollback policy isn't None
    if self.__rollback == None and self.__evolve == None:
      raise RuntimeError, "either the 'rollback' or 'evolve' must be defined"
    if self.__rollback <> None and self.__evolve <> None:
      raise RuntimeError, "either the 'rollback' or 'evolve' must be defined"
    # check that the exercise policy can only be bound with the evolve
    if self.__exercise <> None and self.__rollback <> None:
      raise RuntimeError, "the 'exercise' cannot be bound to the 'rollback'"

  def requestor(self):
    return self.__requestor

  def state(self):
    return self.__state

  def fill(self):
    return self.__fill

  def rollback(self):
    if self.__rollback == None:
      raise RuntimeError, "'rollback' component is undefined"
    return self.__rollback

  def evolve(self):
    if self.__evolve == None:
      raise RuntimeError, "'evolve' component is undefined"
    return self.__evolve

  def exercise(self):
    if self.__exercise == None:
      raise RuntimeError, "'exercise' component is undefined"
    return self.__exercise


   
  
