import sys, os
import unittest

def suite():
    # Loop over all .py files here, except me :)
    try:
        me = __file__
    except NameError:
        me = sys.argv[0]

    me = os.path.abspath(me)
    files = os.listdir(os.path.dirname(me))
    suite = unittest.TestSuite()
    for file in files:
        base, ext = os.path.splitext(file)
        if ext=='.py' and os.path.basename(me) != file:
            mod = __import__(base)
            if hasattr(mod, "suite"):
                test = mod.suite()
            else:
                test = unittest.defaultTestLoader.loadTestsFromModule(mod)
            suite.addTest(test)
    return suite

class CustomLoader(unittest.TestLoader):
  def loadTestsFromModule(self, module):
    return suite()

def _usage():
  print "usage: %s opts" % sys.argv[0]
  print "Try `python %s -h' for more information." % sys.argv[0]

def _help():
    print "usage: %s [-v=<number>]" % sys.argv[0]
    print "Options and arguments:"
    print "-h (--help)            : print this help message and exit"
    print "-v arg (--verbosity)   : more or less output"

if __name__=='__main__':
  unittest.TestProgram(testLoader=CustomLoader())(argv=sys.argv)
