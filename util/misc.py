def isStrUnicode(a):
  return isinstance(a, str) or isinstance(a, unicode)

## give a value *a* and a type *t*
## check if a is of type t
## if not, try to convert a to type t
## return: (True, None) if a is type t
## return: (True, a) if input a is not type t, but has been coverted.
## return: (False, None) if input a is not type t, and cannot be converted.
def fix_instance(a, t):
  # if a is not an instance of t, try to fix it
  # return (ok, a) 
  # ok=False means cannot be fixed
  # ok=True means it is fixed, a is return; OR, a is an instance of t, needs not to fix
  if not isinstance(t, type):
    print "input error: needs a type"
    return False, None
  if isinstance(a, t):
    return True, None
  # try to fix it
  if t == str:
    try:
      a = str(a)
    except:
      return False, None
  elif t == int:
    try:
      if isStrUnicode(a) and ',' in a:
        # handle the case '3,128'
        a = a.replace(',','')
      if isStrUnicode(a) and '.' in a:
        # handle the case '76.00'
        a = a.split('.')[0]
      a = float(a)
      a = int(a)
    except:
      return False, None
  elif t == float:
    try:
      if isStrUnicode(a) and ',' in a:
        # handle the case '3,128'
        a = a.replace(',','')
      a = float(a)
    except:
      return False, None
  else:
    return False, None
  return True, a
