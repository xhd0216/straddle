import datetime

def isStrUnicode(a):
  return isinstance(a, str) or isinstance(a, unicode)

## give a value *a* and a type *t*
## check if a is of type t
## if not, try to convert a to type t
## return: (True, None) if a is type t
## return: (True, a) if input a is not type t, but has been coverted.
## return: (False, None) if input a is not type t, and cannot be converted.
def fix_instance(a, t):
  """ convert input a to type t """
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
  if t == str: # we don't support unicode  yet, str only
    if isStrUnicode(a):
      # convert unicode
      try:
        a = a.encode('UTF-8')
      except:
        # cannot fix, but keep it...
        return True, None
      return True, a
    # otherwise      
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
      if isStrUnicode(a):
        if ',' in a:
          # handle the case '3,128'
          a = a.replace(',','')
      a = float(a)
    except:
      return False, None
  else:
    return False, None
  return True, a

date_origin = datetime.date(1970, 1, 1)

def getRoundDate(d):
  try:
    r =  datetime.date(d.year, d.month, d.day)
  except:
    print "format error"
    return None
  return r
# return today's date
def getNowDate():
  now = datetime.datetime.now()
  return getRoundDate(now)

# give a date (or datetime), return the seconds (of the date, not time)
def getTimeSecond(date):
  try: 
    t = getRoundDate(date)
    r = (t - date_origin).total_seconds()
  except:
    return None
  return int(r)

# return the seconds of some days after today
def getDayAfter(days):
  if not isinstance(days, int):
    return None      
  return getTimeSecond(getNowDate() + datetime.timedelta(days=days))

# get a range of days in range(a,b) = [a,b), in seconds.
def getDayAfterRange(a, b):
  if not isinstance(a, int) or not isinstance(b, int):
    return []
  r = getNowDate()                           
  return [r + datetime.timedelta(days=i) for i in range(a,b)]
  
