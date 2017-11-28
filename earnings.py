import urllib2
from HTMLParser import *
import json

s = 'https://finance.yahoo.com/calendar/earnings'


class earning():
  def __init__(self, misc=None):
    self.data = dict()
    if isinstance(misc, dict):
      for i in misc.keys():
        self.data[i] = misc[i]
  def isValid(self):
    fields = {'symbol':str, 'eps':float}
    for k in fields.keys():
      if k not in self.data or self.data[k] == None:
        print "key %s is missing" % k
        return False
      if not isinstance(self.data[k], fields[k]):
        # try to fix it
        a = self.data[k]
        t = fields[k]
        if t == str:
          try:
            a = str(a)
            self.data[k] = a
          except:
            print "data format error: %s is not a string" % k
            return False
        elif t == int:
          try:
            a = float(a)
            a = int(a)
            self.data[k] = a
          except:
            print "data format error: %s is not an integer" % k
            return False
        elif t == float:
          try:
            a = float(a)
            self.data[k] = a
          except:
            print "data format error: %s is not a float" % k
            return False
        else:
          return False
    return True
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
  def setAttr(self, key, value):
    if not isinstance(key, str):
      return
    self.data[key] = value
  def __json__(self):
    return json.dumps(self.data)
    
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
  def __json__(self):
    js = '{\"data\":[' + ','.join([i.__json__() for i in self.data]) + ']}'
    return js
a = urllib2.urlopen(s)
b = a.read()
j = earningParser()
j.feed(b)
for i in j.data:
  print i.__json__()
print j.__json__()
