def register_com_class(classobj):
  import win32com.server.register
  win32com.server.register.UseCommandLine(classobj)

def raise_com_exception(e):
  from win32com.server.exception import COMException
  raise COMException(desc="ppf error : \""+str(e)+"\"", scode=0x80040201)

def retrieve(module, server, tag, what):
  exec("from %s import %s "% (module, server))
  table=eval(server+"._"+what)
  if not table.has_key(tag):
    raise RuntimeError, "\""+tag+"\" not found"
  return table[tag]

def to_ppf_date(t):
  import ppf.date_time
  return ppf.date_time.date(t.year, t.month, t.day)
