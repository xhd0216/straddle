from HTMLParser import HTMLParser
import urllib2
import ssl
import os
from straddle.strategy import *
data_place_holder = '-'
## example: index/vix, stock/aapl, fund/dust
market_watcher_url = 'https://www.marketwatch.com/investing/%s/%s/options'

table_headings=["Symbol", "Last", "Change", "Vol", "Bid", "Ask", "OpenInt", "Strike", "Symbol", "Last", "Change", "Vol", "Bid", "Ask", "OpenInt"]
def getCallAskIndex():
  return 5
def getPutAskIndex():
  return 13
def getCallBidIndex():
  return 4
def getPutBidIndex():
  return 12
def getStrikeIndex():
  return 7
def getCallOpenIntIndex():
  return 6
def getPutOpenIntIndex():
  return 14
def getAttr(attrs, key):
  for x in attrs:
    if key == x[0]:
      return x[1]
  return None

def getCallStrikeInstance(symb, exp, row):
  miscc = {'underlying':symb,
            'strike':row[getStrikeIndex()],
            'expiration':exp,
            'call':True}
  oi = row[getCallOpenIntIndex()]
  ca = row[getCallAskIndex()]
  cb = row[getCallBidIndex()]
  if oi != data_place_holder:
    miscc['open_int'] = oi
  if ca != data_place_holder:
    miscc['ask'] = ca
  if cb != data_place_holder:
    miscc['bid'] = cb
  r = Strike(misc=miscc)
  return r 
def getPutStrikeInstance(symb, exp, row):
  miscc = {'underlying':symb,
            'strike':row[getStrikeIndex()],
            'expiration':exp,
            'call':False}
  oi = row[getPutOpenIntIndex()]
  ca = row[getPutAskIndex()]
  cb = row[getPutBidIndex()]
  if oi != data_place_holder:
    miscc['open_int'] = oi
  if ca != data_place_holder:
    miscc['ask'] = ca
  if cb != data_place_holder:
    miscc['bid'] = cb
  r = Strike(misc=miscc)
  return r 
class MWFormParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.form_links=[]
  def handle_starttag(self, tag, attrs):
    if tag == 'form':
      a = getAttr(attrs, 'action')
      if a != None:
        self.form_links.append(a)
  def getLinks(self):
    return self.form_links

class MarketWatcherParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.begin_table = False
    self.begin_row = False
    self.stock_price = False
    self.row = []
    self.begin_cell = False
    self.b_expire = False
    self.data = []
    self.current_price = 0
    self.near_strike = []
    self.expiration_date = ''
    self.symbol = ''
  def setSymbol(self, s):
    self.symbol = s
  def doXHRtable(self, b=True):
    self.begin_table=b
  def handle_starttag(self, tag, attrs):
    if tag == 'table':
      a = getAttr(attrs, 'class')
      if a != None and 'optiontable' in a:
        self.begin_table = True
    elif tag == 'tr' and self.begin_table:
      a = getAttr(attrs, 'class')
      if a != None and 'heading' in a and a.find('colhead') == -1:
        # meet heading
        # do nothing
        pass
      elif a != None and 'aright' in a:
        # meet a row
        self.row = []
        self.begin_row = True
      elif a != None and 'stockprice' in a:
        # meet stock price
        self.row = []
        self.stock_price = True
    elif tag == 'td' and (self.stock_price or self.begin_row):
      a = getAttr(attrs, 'class')
      if 'acenter' not in a:
        self.begin_cell = True
      self.row.append(data_place_holder)
    elif tag == 'td':
      a = getAttr(attrs, 'colspan')
      if a != None:
        a = int(a)
        if a > 10: # a == len(table_headings)
          self.b_expire = True
  def handle_endtag(self, tag):
    if tag == 'table':
      self.begin_table = False
    if tag == 'tr':
      self.begin_row = False
      self.stock_price = False
      if self.begin_table:
        if len(self.row) == len(table_headings):
          call = getCallStrikeInstance(self.symbol, self.expiration_date, self.row)
          put = getPutStrikeInstance(self.symbol, self.expiration_date, self.row)
          self.data.append(call)
          self.data.append(put)
          print self.row
          self.row = []
    if tag == 'td' and self.begin_cell:
      self.begin_cell = False
    if tag == 'td' and self.b_expire:
      self.b_expire = False
  def handle_data(self, data):
    expire_str = 'Expires '
    if self.b_expire and expire_str in data:
      print "*****", data[data.find(expire_str) + len(expire_str):], "*****"
    if self.begin_cell:
      if self.begin_row:
        ts = data.strip()
        self.row[-1] = ts
      if self.stock_price:
        if 'Current price' not in data:
          self.current_price = float(data)
          print '=====', data, '====='


def getOptionMW():
  symb = 'aapl'
  f = urllib2.urlopen(market_watcher_url % ('stock', symb))
  print f.getcode()
  g = f.read()
  encoding=f.headers['content-type'].split('charset=')[-1]
  g = unicode(g, encoding)
  f.close()
  p = MWFormParser()
  p.feed(g)
  q = MarketWatcherParser()
  q.doXHRtable()
  q.setSymbol(symb)
  for u in p.getLinks():
    f = urllib2.urlopen('https://www.marketwatch.com' + u)
    g = f.read()
    code = f.getcode()
    f.close()
    if code != 200:
      print 'error when loading url', u
      continue
    #q = MarketWatcherParser()
    #q.doXHRtable()
    q.feed(g)
  fi = open('data_output.txt', 'w')
  for i in q.data:
    fi.write(i.__json__())
  fi.close()
getOptionMW()
