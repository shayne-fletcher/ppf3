import ppf.date_time

def generate_date_tuples(
   start
 , end
 , period = 6
 , duration = ppf.date_time.months
 , shift_method  = ppf.date_time.modified_following
 , basis = ppf.date_time.basis_act_360
 , holiday_centers = None
 , *arguments
 , **keywords):
  '''
    >>> from ppf import *
    >>> from ppf.date_time import *
    >>> flows = generate_date_tuples(
    ...   start  = date(2007, Jun, 29)
    ...   , end  = date(2017, Jun, 29)
    ...   , resolution = date_resolutions.months
    ...   , period = 6
    ...   , shift_method = shift_convention.modified_following
    ...   , basis = "ACT/360")
    >>> for f in flows:
    ...  print "%s, %s" % f
    2007-Jun-29, 2007-Dec-31
    2007-Dec-31, 2008-Jun-30
    2008-Jun-30, 2008-Dec-29
    2008-Dec-29, 2009-Jun-29
    2009-Jun-29, 2009-Dec-29
    2009-Dec-29, 2010-Jun-29
    2010-Jun-29, 2010-Dec-29
    2010-Dec-29, 2011-Jun-29
    2011-Jun-29, 2011-Dec-29
    2011-Dec-29, 2012-Jun-29
    2012-Jun-29, 2012-Dec-31
    2012-Dec-31, 2013-Jun-28
    2013-Jun-28, 2013-Dec-30
    2013-Dec-30, 2014-Jun-30
    2014-Jun-30, 2014-Dec-29
    2014-Dec-29, 2015-Jun-29
    2015-Jun-29, 2015-Dec-29
    2015-Dec-29, 2016-Jun-29
    2016-Jun-29, 2016-Dec-29
    2016-Dec-29, 2017-Jun-29
  '''
  i, day  = 0, start
  flows = []
  shift = ppf.date_time.shift
  while day < end:
    flow_start = shift(
            start + duration(i*period)
          , shift_method, holiday_centers)
    flow_until = shift(
            start + duration((i + 1)*period)
          , shift_method, holiday_centers)
    flows.append((flow_start, flow_until))
    day = flow_until
    i += 1

  return flows

def _test():
  import doctest
  doctest.testmod()

if __name__ == '__main__':
    _test()
