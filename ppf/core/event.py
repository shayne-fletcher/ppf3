import string
class event_type(object):
    flow, exercise = (1, -1)

class pay_event(object):
  def __init__(
        self
      , flow
      , pay_rcv
      , leg_id
      , reset_id):
    self.__flow    \
  , self.__pay_rcv \
  , self.__leg_id \
  , self.__reset_id = flow, pay_rcv, leg_id, reset_id

  def flow(self) : return self.__flow
  def pay_recieve(self) : return self.__pay_rcv
  def leg_id(self) : return self.__leg_id
  def reset_id(self) : return self.__reset_id
  def pay_currency(self) : return self.__flow.pay_currency()
  def __str__(self) :
    s = "payment [%s, %s, %s, %s], " % \
         (self.__pay_rcv, self.__leg_id, self.__reset_id, str(self.__flow))
    return s

class exercise_event(object):
  def __init__(
        self
      , exercise_opportunity
      , exercise_type):
    self.__exercise_opportunity  \
  , self.__exercise_type = exercise_opportunity, exercise_type
  def exercise_type(self) : return self.__exercise_type
  def exercise_opportunity(self) : return self.__exercise_opportunity
  def pay_currency(self) : return self.__exercise_opportunity.fee_currency()
  def __str__(self) :
    s = "exercise [%s, %s], " % \
        (self.__exercise_type, str(self.__exercise_opportunity))
    return s

def is_pay_event(event): return isinstance(event, pay_event)
def is_exercise_event(event): return isinstance(event, exercise_event)
