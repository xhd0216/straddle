"""
  define various utility functions
"""
import datetime
import random


def binary_search(data, target, start, end, f=lambda x: x):
  """ return index i in data that is bigger than target """
  if start > end or start < 0 or end >= len(data):
    return None
  if f(data[start]) > target:
    return start
  if f(data[end]) <= target:
    return None
  if start == end:
    return start
  mid = (end + start) / 2
  if f(data[mid]) > target:
    if f(data[mid-1]) <= target:
      return mid
    return binary_search(data, target, start, mid-1, f)
  if f(data[mid]) == target:
    return mid + 1
  return binary_search(data, target, mid+1, end, f)


def test_binary_search():
  """ test binary_search """
  arr = sorted(random.sample(range(1, 100), 80))
  tests = random.sample(range(1, 100), 20) + [-2, -1, 0, 99, 100, 101]
  for x in tests:
    found = False
    for i in range(len(arr)):
      if arr[i] > x:
        assert i == binary_search(arr, x, 0, len(arr)-1)
        found = True
        break
    if not found:
      assert binary_search(arr, x, 0, len(arr)-1) is None


def isStrUnicode(a):
  """ if input is string or unicode """
  return isinstance(a, str) or isinstance(a, unicode)


# date formats that are supported
DATE_FORMATS = ['%Y-%m-%d',
                '%b %d, %Y',
                '%B %d, %Y',
                '%Y%m%d',
                '%Y-%m-%d, %H:%M:%S',]

def fix_datetime(a):
  """ convert a str or int to date """
  if isStrUnicode(a):
    for df in DATE_FORMATS:
      try:
        res = datetime.datetime.strptime(a, df)
      except:
        pass
      else:
        return res
  elif isinstance(a, int):
    # case 1, unix epoch time 1522387739
    if a > 1022387739:
      return datetime.datetime.fromtimestamp(a)
    # case 2, YYYYMMDD
    elif a > 10000101 and a <= 99991231:
      return datetime.datetime(a / 10000, (a/100)%100, a % 100)
  elif isinstance(a, datetime.date):
    # date is not datetime, datetime is date (weird)
    return datetime.datetime(a.year, a.month, a.day)
  return None


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
  assert isinstance(t, type)

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
  elif t == datetime.datetime or t == datetime.date:
    res = fix_datetime(a)
    if res:
      if t == datetime.date:
        return True, res.date()
      return True, res
    else:
      return False, None
  elif t == bool:
    if isinstance(a, int):
      return True, a > 0
    if isinstance(a, str):
      return True, a.lower() == 'true'
    else:
      return False, None
  else:
    return False, None
  return True, a

date_origin = datetime.date(1970, 1, 1)

def getRoundDate(d):
  """ given a datetime, return only the date """
  return datetime.date(d.year, d.month, d.day)

def getNowDate():
  """ return today's date """
  now = datetime.datetime.now()
  return getRoundDate(now)

def getTimeSecond(date):
  """ give a date (or datetime), return the seconds (of the date, no time) """
  t = getRoundDate(date)
  r = (t - date_origin).total_seconds()
  return int(r)

def getDayAfter(days):
  """ return the seconds of some days after today """
  return getTimeSecond(getNowDate() + datetime.timedelta(days=days))

def getDayAfterRange(a, b):
  """ get a range of days in range(a,b) = [a,b), in seconds. """
  if not isinstance(a, int) or not isinstance(b, int):
    return []
  r = getNowDate()
  return [r + datetime.timedelta(days=i) for i in range(a,b)]
