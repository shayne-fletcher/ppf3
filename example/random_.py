import random, sys, getopt

def _print_gauss():
  g = random.Random(1234)
  print [g.gauss(mu = 0, sigma = 1) for i in range(100)]

def _print_lognormal_variate():
  g = random.Random(1234)
  print [g.lognormvariate(mu = 0, sigma = 1) for i in range(100)]

def _usage():
  print "usage: %s" % sys.argv[0]
  print "Try `python %s -h' for more information." % sys.argv[0]

def _help():
  print "usage: %s" % sys.argv[0]
  print "-h (--help)            : print this help message and exit"
  print "-v (--version)         : print the version number and exit"

if __name__ == '__main__':
  try:
   opts, args, = getopt.getopt(sys.argv[1:], "vh", ["version", "help", ])
  except getopt.GetoptError:
    _usage()
    sys.exit(2)
  for o, a in opts:
    if o in ("-h", "--help"):
      _help()
      sys.exit()
    if o in ("-v", "--version"):
      print "'%s', Version 0.0.0" % sys.argv[0]
      sys.exit()
  _print_gauss()
  _print_lognormal_variate()
