"""
  base objects class
"""
import datetime
import json
import logging
from util.misc import *


DEFAULT_DATE_FORMAT_STR = '%Y-%m-%d'
DEFAULT_TIME_FORMAT_STR = '%Y-%m-%d %H:%M:%S'

def obj_convert(o):
  """ convert objects to json serializables """
  if isinstance(o, datetime.datetime):
    if o.hour == 0 and o.minute == 0:
      # only print date
      return datetime.datetime.strftime(o, DEFAULT_DATE_FORMAT_STR)
    else:
      return datetime.datetime.strftime(o, DEFAULT_TIME_FORMAT_STR)
  # note: date is not datetime, datetime is date.
  elif isinstance(o, datetime.date):
    return datetime.date.strftime(o, DEFAULT_DATE_FORMAT_STR)
  elif hasattr(o, 'data'):
    return o.data
  else:
    return str(o)


class objects():
  """ base objects class """
  def __init__(self):
    self.fields = dict()     # required fields, (key, type) must match
    self.auxiliary = dict()  # non-required fields, (key, type) must match
    self.data = dict()

  def __json__(self, indent=4, sort_keys=True):
    """ dump data to json file """
    if not self.isValid():
      logging.error('object is not valid')
    return json.dumps(self.data,
                      sort_keys=sort_keys,
                      indent=indent,
                      default=obj_convert)

  def __validate__(self, k, t, required=True):
    """ validate a single key """
    assert isinstance(k, str)
    assert isinstance(t, type)

    if k not in self.data:
      if required:
        logging.error('missing required key %s', k)
      return not required
    b, a = fix_instance(self.data[k], t)
    if b == False:
      logging.error("type error, key=%s, val=%s, expected type=%s", k, a, t)
    elif a != None:
      # fix it.
      self.data[k] = a
    return b

  def isValid(self):
    """ validate all keys in data """
    if self.data is None:
      logging.error("no data")
      return False

    for k in self.fields:
      if k not in self.data:
        logging.error("key %s is missing", k)
        return False
      b = self.__validate__(k, self.fields[k])
      if not b:
        logging.error("wrong type: key %s, value %s, type %s", k, str(self.data[k]), str(self.fields[k]))
        return False

    for k in self.auxiliary.keys():
      b = self.__validate__(k, self.auxiliary[k], required=False)
      if not b:
        logging.error("wrong type: key %s, value %s, type %s", k, str(self.data[k]), str(self.auxiliary[k]))
        return False
    return True

  def getKey(self, key, default_value=None):
    """ get key from data """
    return self.data.get(key, default_value)

  def addKey(self, key, val, replace=True):
    """ write (key, val) to data """
    b = True
    a = None
    if not replace and key in self.data:
      # don't replace
      return False
    if key in self.fields:
      b, a = fix_instance(val, self.fields[key])
    elif key in self.auxiliary:
      b, a = fix_instance(val, self.auxiliary[key])
    if not b:
      return b
    if a != None:
      val = a
    self.data[key] = val
    return True

  def addField(self, key, tp, required):
    """ add a field """
    assert isinstance(key, str)
    assert isinstance(tp, type)
    assert key not in self.data
    assert key not in self.auxiliary
    assert key not in self.fields

    if not required:
      self.auxiliary[key] = tp
    else:
      self.fields[key] = tp
