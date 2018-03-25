import json
from datetime import *
from lib.objects import objects
from util.misc import *

default_underlying = "SPY"
default_strike = 100.0
default_expiration = "Dec 31, 2099"
default_call = True
default_misc = None

default_date_format = "%b %d, %Y" ## Nov 11, 2017

strike_field = {'underlying':str, 
                'strike':float,
                'expiration':str,
                'call':bool}
strike_auxiliary = {'bid':float,
                    'ask':float,
                    'open_int':int,
                    'query_time':datetime}
class Strike(objects):
  def __init__(self, 
        misc=None,
        underlying=None, 
        strike=None, 
        expiration=None,  ## str
        call=None,
				query_time=None):
    objects.__init__(self)
    self.fields = strike_field
    self.auxiliary = strike_auxiliary
    self.error = None
    if isinstance(misc, dict):
      for k in misc.keys():
        self.data[k] = misc[k]
    ## this four arguments overrides entries in misc
    if strike != None:
      self.data['strike'] = strike
    if expiration != None:    
      self.data['expiration'] = expiration
    if call != None:
      self.data['call'] = call
    if underlying != None:
      self.data['underlying'] = underlying
    if query_time != None:
      self.data['query_time'] = query_time
    if 'query_time' not in self.data or self.data['query_time'] is None:
      self.data['query_time'] = datetime.datetime.now()
    if not self.isValid():
      self.data = None
  def getStrike(self):
    return self.getKey('strike')
  def isCall(self):
    if not self.data or 'call' not in self.data or self.data['call'] == None:
      return None
    return self.getKey('call')
  def getUnderlying(self):
    return self.getKey('underlying')
  def getExpirationStr(self):
    return self.getKey('expiration')
  def getExpirationDate(self, fm=default_date_format):
    s = self.getExpirationStr()
    if s == None:
      return None
    try:
      dt = datetime.datetime.strptime(s, fm)
    except:
      self.error = "wrong date time formate"
      return None  
    return dt
  def getAsk(self):
    return self.getKey('ask')
  def getBid(self):
    return self.getKey('bid')
  def getCurrentPrice(self):
    a = self.getStrike()
    b = self.isCall()
    c = self.getUnderlying()
    d = self.getExpirationDate()
    if a == None or b == None or c == None or d == None:
      return None
    ### make quote to database
    return 1.0
  def getUnderlyingPrice(self):
    ud = self.getUnderlying()
    if ud == None:
      return None
    return 2.15
  def hasPosition(self):
    if not self.data or 'position' not in self.data or self.data['position'] == None:
      return False
    a = self.data['position']
    if not isinstance(a, int):
      try:
        a = int(float(a))
        self.data['position'] = a
      except:
        ## log this event
        self.error = "invalid position"
        self.data['position'] = None
        return False
    return True
  def getPosition(self):
    if not self.hasPosition():
      return None
    return self.data['position']
  def setPosition(self, pos, diff=True):
    ## set position and return new position
    if self.data == None:
      return None
    a = pos
    if not isinstance(a, int):
      try:
        a = int(float(a))
      except:
        return None
    if not self.hasPosition():
      self.data['position'] = a
      return a
    else:
      if diff:
        self.data['position'] += a
      else:
        self.data['position'] = a
    return self.data 
  def setAsk(self, m):
    b, a = fix_instance(m, float)
    if not b:
      m = 0.0
    elif a != None:
      m = a
    return self.addKey('ask', m) 
  def setBid(self, m):
    b, a = fix_instance(m, float)
    if not b:
      m = 0.0
    elif a != None:
      m = a
    return self.addKey('bid', m)
  def setOpenInt(self, m):
    b, a = fix_instance(m, int)
    if not b:
      m = 0
    elif a!= None:
      m = a
    return self.addKey('open_int', m)
def parseStrike(s):
	try:
		a = json.loads(s)
		r = Strike(misc=a)
	except:
		return None
	return r

strategy_must = {
  "name":str,
  "strikes":list,
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
  def __json__(self):
    # TODO: this does not support indent in json print
    s = "{\"name\":\"%s\", \"current_price\":%s, \"legs\":[" % (self.getName(), self.getUnderlyingPrice())
    s += ','.join([i.__json__() for i in self.getLegs()]) 
    s += "]}"
    return s
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
