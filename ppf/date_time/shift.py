from ppf_date_time import *
from is_business_day import *
from shift_convention import *

def shift(t, method, holiday_centres=None):
  d = date(t)
  if not is_business_day(d):
    if method == shift_convention.following:
      while not is_business_day(d, holiday_centres):
        d = d + days(1)
    elif method == shift_convention.modified_following:
      while not is_business_day(d, holiday_centres):
        d = d + days(1)
      if d.month().as_number() != t.month().as_number():
          d = date(t)
          while not is_business_day(d):
            d = d - days(1)
    elif method == shift_convention.preceding:
      while not is_business_day(d, holiday_centres):
        d = d - days(1)
    elif method == shift_convention.modified_preceding:
      while not is_business_day(d, holiday_centres):
        d = d - days(1)
      if d.month().as_number() != t.month().as_number():
        while not is_business_day(d, holiday_centres):
          d = d + days(1)
    else: raise RuntimeError ("Unsupported method")

  return d
    
    
  
