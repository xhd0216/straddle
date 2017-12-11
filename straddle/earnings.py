import urllib2
from HTMLParser import *
import json
from objects import objects

yahoo_earning_url = 'https://finance.yahoo.com/calendar/earnings'


class earning(objects):
  def __init__(self, misc=None):
    objects.__init__(self)
    self.addRequiredField('symbol', str)
    # eps is not required, could be '-'
    # self.addRequiredField('eps', float)
    if isinstance(misc, dict):
      for i in misc.keys():
        self.data[i] = misc[i]
  def setSymbol(self, symbol):
    if isinstance(symbol, str):
      self.data['symbol'] = symbol
  def setEPS(self, eps):
    try:
      a = float(eps)
    except:
      self.data['eps'] = None
      return
    self.data['eps'] = a
  def getSymbol(self):
    if self.isValid():
      return self.data['symbol']
    return None
  def getEPS(self):
    return self.getKey('EPS')
class earningParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.meet_eps = False
    self.data = []
    self.e = None
  def hasAttrs(self, attrs, key):
    for x in attrs:
      if key == x[0]:
        return True, x[1]
    return False, None
  def handle_starttag(self, tag, attrs):
    if tag == 'td':
      b, c = self.hasAttrs(attrs, 'class')
      if b and c[:9] == 'data-col3':
        self.meet_eps = True
    elif tag == 'a':
      b, c = self.hasAttrs(attrs, 'data-symbol')
      if b:
        self.e = earning()
        self.e.setSymbol(c)
  def handle_data(self, data):
    if self.meet_eps:
      if self.e:
        self.e.setEPS(data)
        self.data.append(self.e)
      self.e = None
      self.meet_eps = False
  def getData(self):
    self.data.sort(key=lambda e: e.getSymbol())
    return self.data
  def __json__(self):
    self.data.sort(key=lambda e: e.getSymbol())
    js = '{\"data\":[' + ','.join([i.__json__() for i in self.data]) + ']}'
    return js


