import json
from util.misc import *

class objects():
  def __init__(self):
    self.fields = dict()     # required fields, (key, type) must match
    self.auxiliary = dict()  # non-required fields, (key, type) must match
    self.data = dict()
  def __json__(self):
    if not self.isValid():
      return '{}'
    return json.dumps(self.data, sort_keys=True, indent=3)
  def __validate__(self, k, required=True):
    # validate single key
    if not isinstance(k, str):
      # invalid key
      return False
    if required and k not in self.fields:
      # this key is not required
      return k in self.data
    if k not in self.data or self.data[k] == None:
      # key is required but data is missing
      return not required
    if required:
      b, a = fix_instance(self.data[k], self.fields[k])
    else:
      b, a = fix_instance(self.data[k], self.auxiliary[k])
    if b == False:
      return b
    if b and a != None:
      # fix it.
      self.data[k] = a
    return True
  def isValid(self):
    if self.data == None:
      return False
    for k in self.fields.keys():
      if k not in self.data or self.data[k] == None:
        print "key %s is missing" % k
        return False
      b = self.__validate__(k)
      if not b:
        print "wrong type for key %s" % k
        return False
    for k in self.auxiliary.keys():
      b = self.__validate__(k, required=False)
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
    b = True
    a = None
    if key in self.fields:
      b, a = fix_instance(val, self.fields[key])
    elif key in self.auxiliary:
      b, a = fix_instance(val, self.auxiliary[key])
    if b == False:
      return b
    if a != None:
      val = a
    self.data[key] = val
    return True
  def addNoneRequiredField(self, key, tp, force=False):
    if not isinstance(key, str):
      return False
    if not isinstance(tp, type):
      return False
    if key in self.fields:
      # don't change key fields
      return False
    if key in self.auxiliary:
      if force != True:
        return False
    self.auxiliary[key] = tp
    return True
  def addRequiredField(self, key, tp, force=False):
    if not isinstance(key, str):
      return False
    if not isinstance(tp, type):
      return False
    if key in self.fields:
      # field already set
      if force != True:
        return False
    self.fields[key] = tp
    return True
