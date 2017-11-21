import json
from datetime import datetime

default_underlying = "SPY"
default_strike = 100.0
default_expiration = "Dec 31, 2099"
default_call = True
default_misc = None

default_date_format = "%b %d, %Y" ## Nov 11, 2017
default_expiration_date = datetime.strptime(default_expiration, default_date_format)

class Strike():
  def __init__(self, 
        misc=None,
        underlying=None, 
        strike=None, 
        expiration=None,  ## str
        call=None):
    self.data = dict() 
    self.error = None
    if misc and isinstance(misc, dict):
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
    if not self.__validate__():
      self.data = None
  def __validate__(self):
    if 'strike' not in self.data:
      self.error = "strike is none"
      return False
    elif not isinstance(self.data['strike'], float):
      try:
        self.data['strike'] = float(self.data['strike'])
      except:
        self.error = "strike is not float"
        return False
    if 'expiration' not in self.data or self.data['expiration'] == None:
      self.error = "expiration"
      return False
    """
    dt = self.data['expiration']
    if not isinstance(dt, datetime):
      try:
        dt = datetime.strptime(dt, default_date_format)
        self.data['expiration'] = dt
      except:
        self.error = "cannot parse expiration"
        return False
    """
    if 'call' not in self.data or self.data['call'] == None:
      self.error = "call is null"
      return False
    if not isinstance(self.data['call'], bool):
      if isinstance(self.data['call'], str):
        s = self.data['call']
        if s.lower() == 'call' or s.lower() == 'true':
          self.data['call'] = True
        elif s.lower() == 'put' or s.lower() == 'false':
          self.data['call'] = False
        else:
          self.error = "invalid call str"
          return False
      else:
        self.error = "call is none"
        return False
    if 'underlying' not in self.data or self.data['underlying'] == None:
      self.error = "underlying is missing"
      return False
    return True
  def isValid(self):
    return self.data != None
  def __json__(self):
    if not self.isValid():
      if self.error != None:
        return '{\"error\": \"%s\"}' % self.error
      else:
        return '{\"error\": null}'
    return json.dumps(self.data)
  def getStrike(self):
    if self.data == None or 'strike' not in self.data or self.data['strike'] == None:
      return None
    return self.data['strike']
  def isCall(self):
    if not self.data or 'call' not in self.data or self.data['call'] == None:
      return None
    return True
  def getUnderlying(self):
    if not self.data or 'underlying' not in self.data or self.data['underlying'] == None:
      return None
    return self.data['underlying']
  def getExpirationStr(self):
    if not self.data or 'expiration' not in self.data or self.data['expiration'] == None:
      return None
    return self.data['expiration']
  def getExpirationDate(self):
    s = self.getExpirationStr()
    if s == None:
      return None
    try:
      dt = datetime.strptime(s, default_date_format)
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
    self.strikes = []
    self.name = "unspecified"
  def __str__():
    return str(self.price)
  def __json__(self):
    s = "{\"name\":\"%s\", \"data\":[" % self.getName()
    for i in range(len(self.strikes)):
      if hasattr(self.strikes[i], "__json__"):
        s += self.strikes[i].__json__()
      else:
        s += "null"
      if i != len(self.strikes) - 1:
        s += ","
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
  def __init__(self, price1=None, expiration=None, position=None):
    strategies.__init__(self)
    self.strikes = []
    self.name = "straddle"
    if not price1 or not expiration:
      self.strikes = [None] * 2
    else:
			if isinstance(price1, list):
				p = price1[0]
			else:
				p = price1
			if isinstance(expiration, list):
				e = expiration[0]
			else:
				e = expiration
			if not posistion:
				po = 100
			elif isinstance(position, list):
				po = position[0]
			else:
				po = position
			self.strikes.append(Strike(p, e, "call"))
			self.strikes.append(Strike(p, e, "put"))
  def __str__(self):
    return str(self.price) + str(self.strike)
