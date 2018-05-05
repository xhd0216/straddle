import datetime
import json
import logging

from lib.objects import objects
from util.misc import *

default_underlying = "SPY"
default_strike = 100.0
default_expiration = "Dec 31, 2099"
default_call = True
default_misc = None

default_date_format = "%Y-%m-%d"

strike_field = {'underlying':str,
                'strike':float,
                'expiration':datetime.date,
                'price':float,
                'is_call':bool}

strike_auxiliary = {'bid':float,
                    'ask':float,
                    'last':float,
                    'open_int':int,
                    'query_time':datetime.datetime,
                    'position':int}


class Strike(objects):
  def __init__(self, misc):
    objects.__init__(self)
    self.fields = strike_field
    self.auxiliary = strike_auxiliary
    if isinstance(misc, dict):
      for k in misc.keys():
        self.data[k] = misc[k]

  def getTimeToExp(self, current=None):
    if current is None:
      current = self.getKey('query_time')
    if current is None:
      current = datetime.datetime.now()
    return (self.getExpirationDate() - current.date()).days

  def getStrike(self):
    return self.getKey('strike')

  def isCall(self):
    return self.getKey('is_call')

  def getUnderlying(self):
    return self.getKey('underlying')

  def getExpirationStr(self, format_str=default_date_format):
    return datetime.datetime.strftime(self.getKey('expiration'), format_str)

  def getExpirationDate(self):
    res = self.getKey('expiration')
    if isinstance(res, datetime.datetime):
      return res.date()
    return res

  def getAsk(self):
    return self.getKey('ask')

  def getBid(self):
    return self.getKey('bid')

  def getPosition(self):
    return self.getKey('position')

  def setPosition(self, pos, diff=True):
    ## set position
    assert isinstance(pos, int)
    if diff:
      if 'position' not in self.date:
        self.data['position'] = 0
      self.data['position'] += pos
    else:
      self.data['position'] = pos

  def setAsk(self, m):
    return self.addKey('ask', m)

  def setBid(self, m):
    return self.addKey('bid', m)

  def setOpenInt(self, m):
    return self.addKey('open_int', m)


def create_strike(misc, underlying=None, strike=None, expiration=None,
                  is_call=None, price=None, query_time=None):
  """ create a strike """
  # create dictionary
  # 1, get all inputs (underlying, ...)
  local = locals()
  del local['misc']
  # 2, create dictionary
  res = misc if isinstance(misc, dict) else {}
  # 3, update dictionary
  for k in local:
    if local[k] is not None:
      res[k] = local[k]
  # 4, check required fields
  for k in strike_field:
    if k not in res:
      logging.error('missing required field %s', k)
      return None
    if not isinstance(res[k], strike_field[k]):
      b, a = fix_instance(res[k], strike_field[k])
      if not b:
        logging.error("required field %s error %s, type %s", k, res[k], type(res[k]))
        return None
      res[k] = a
  # 5, check auxiliary fields
  for k in strike_auxiliary:
    if k in res and not isinstance(res[k], strike_auxiliary[k]):
      b, a = fix_instance(res[k], strike_auxiliary[k])
      if not b:
        logging.error("auxiliary field %s error %s", k, res)
        return None
      res[k] = a
  # 6, return
  return Strike(res)


def parse_strike(s):
  a = json.loads(s)
  assert a
  return create_strike(a)


strategy_must = {
  "name":str,
  "legs":list,
}
strategy_additional = {
  "underlying_price":float,
  "positions":list
}

class strategies(objects):
  def __init__(self):
    objects.__init__(self)
    self.fields = strategy_must
    self.auxiliary = strategy_additional
  def getName(self):
    return self.getKey('name')
  def getStrikes(self):
    return self.getKey('strikes')
  def getLegs(self):
    return self.getStrikes()
  def getUnderlyingPrice(self):
    return self.getKey('underlying_price')

class straddle(strategies):
  def __init__(self, legs=None, price=None):
    strategies.__init__(self)
    self.data['name'] = "straddle"
    if legs != None:
      self.data['strikes'] = legs
    if price != None:
      self.data['underlying_price'] = price
  def getStraddlePrice(self):
    a = self.getStrikes()
    try:
      b = sum([x.getAsk() for x in a])
    except:
      return None
    return b
  def getCurrentPrice(self):
    return self.getKey('underlying_price')
  def getUnderlying(self):
    return self.getLegs()[0].getUnderlying()
  def getExpirationStr(self):
    return self.getLegs()[0].getExpirationStr()
  def getStrike(self):
    return self.getLegs()[0].getStrike()
  def isValid(self):
    if len(self.getLegs()) != 2:
      print "number of legs is not 2"
      return False
    a = self.getLegs()[0]
    b = self.getLegs()[1]
    if not isinstance(a, Strike) or not isinstance(b, Strike):
      print "legs are not strikes"
      return False
    if a.isCall() == b.isCall():
      print "must be one call one put", a.isCall(), b.isCall()
      return False
    if a.getUnderlying() != b.getUnderlying():
      print "must be same underlying stock"
      return False
    if a.getExpirationStr() != b.getExpirationStr():
      print "must be same expiration date"
      return False
    if a.getStrike() != b.getStrike():
      print "must be same strike"
      return False
    return True
