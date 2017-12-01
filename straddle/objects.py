import json

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
      a = float(a)
      a = int(a)
    except:
      return False, None
  elif t == float:
    try:
      a = float(a)
    except:
      return False, None
  else:
    return False, None
  return True, a
  

class objects():
  def __init__(self):
    self.fields = dict()
    self.data = dict()
  def __json__(self):
    if not self.isValid():
      return ''
    return json.dumps(self.data, sort_keys=True)
  def __validate__(self, k):
    # validate single key
    if not isinstance(k, str):
      # invalid key
      return False
    if k not in self.fields:
      # this key is not required
      return k in self.data
    if k not in self.data or self.data[k] == None:
      # key is required but data is missing
      return False
    b, a = fix_instance(self.data[k], self.fields[k])
    if b == False:
      return b
    if b and a != None:
      # fix it.
      self.data[k] = a
    return True
  def isValid(self):
    for k in self.fields.keys():
      if k not in self.data or self.data[k] == None:
        print "key %s is missing" % k
        return False
      b = self.__validate__(k)
      if not b:
        print "wrong type for key %s" % k
        return False
    return True
  def getKey(self, key):
    b = self.__validate__(key)
    if b:
      return self.data[key]
    else:
      return None
  def addKey(self, key, val):
    if key in self.fields:
      b, a = fix_instance(val, self.fields[key])
      if b == False:
        return b
      if a != None:
        val = a
    self.data[key] = val
    return True
  def addRequiredField(self, key, tp):
    if not isinstance(key, str):
      return False
    if not isinstance(tp, type):
      return False
    self.fields[key] = tp
    return True