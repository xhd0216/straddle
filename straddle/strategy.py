import json
from datetime import datetime
from objects import objects

default_underlying = "SPY"
default_strike = 100.0
default_expiration = "Dec 31, 2099"
default_call = True
default_misc = None

default_date_format = "%b %d, %Y" ## Nov 11, 2017
default_expiration_date = datetime.strptime(default_expiration, default_date_format)

strike_field = {'underlying':str, 
                'strike':float,
                'expiration':str,
                'call':bool}
strike_auxiliary = {'bid':float,
                    'ask':float,
                    'open_int':int}
class Strike(objects):
  def __init__(self, 
        misc=None,
        underlying=None, 
        strike=None, 
        expiration=None,  ## str
        call=None):
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
      dt = datetime.strptime(s, fm)
    except:
      self.error = "wrong date time formate"
      return None  
    return dt
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

def parseStrike(s):
	try:
		a = json.loads(s)
		r = Strike(misc=a)
	except:
		return None
	return r

class strategies():
  def __init__(self):
    self.strikes = [] # legs
    self.name = "unspecified"
    self.uPrice = 0.0 # price of underlying
  def __json__(self):
    s = "{\"name\":\"%s\", \"current_price\":%s, \"legs\":[" % (self.getName(), self.uPrice)
    s += ','.join([i.__json__() for i in self.strikes]) 
    s += "]}"
    return s
  def getName(self):
    return self.name
  def getQuotePrice(self):
    su = 0.0
    for s in self.strikes:
			assert isinstance(s, Strike)
			su += s.getCurrentPrice()
    return su
	
class straddle(strategies):
  def __init__(self, legs=None, price=None):
    strategies.__init__(self)
    self.name = "straddle"
    if legs != None:
      self.strikes = legs
    if price != None:
      self.uPrice = price
  def getStraddlePrice(self):
    return self.strikes[0].data['ask'] + self.strikes[1].data['ask']
  def getCurrentPrice(self):
    return self.uPrice
  def getUnderlying(self):
    return self.strikes[0].getUnderlying()
  def getExpirationStr(self):
    return self.strikes[0].getExpirationStr()
  def getStrike(self):
    return self.strikes[0].getStrike()
  def isValid(self):
    if len(self.strikes) != 2:
      print "number of legs is not 2"
      return False
    a = self.strikes[0]
    b = self.strikes[1]
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
