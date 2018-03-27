import argparse
from HTMLParser import HTMLParser
import os
import ssl
import urllib2

from straddle.strategy import *
from util.networks import *

DATA_PLACE_HOLDER = '-'

## example: index/vix, stock/aapl, fund/dust
MATKET_WATCHER_URL = 'https://www.marketwatch.com/investing/%s/%s/options'

TABLE_HEADERS=["Symbol",
               "Last",
               "Change",
               "Vol",
               "Bid",
               "Ask",
               "OpenInt",
               "Strike",
               "Symbol",
               "Last",
               "Change",
               "Vol",
               "Bid",
               "Ask",
               "OpenInt"]


def getCallAsk(row):
  return row[5]


def getPutAsk(row):
  return row[13]


def getCallBid(row):
  return row[4]


def getPutBid(row):
  return row[12]


def getStrike(row):
  return row[7]


def getCallOpenInt(row):
  return row[6]


def getPutOpenInt(row):
  return row[14]


def getAttr(attrs, key):
  for x in attrs:
    if key == x[0]:
      return x[1]
  return None


def getCallStrikeInstance(symb, exp, row):
  miscc = {'underlying':symb,
           'strike':getStrike(row),
           'expiration':exp,
           'call':True}
  oi = getCallOpenInt(row)
  ca = getCallAsk(row)
  cb = getCallBid(row)
  if oi != DATA_PLACE_HOLDER:
    miscc['open_int'] = oi
  if ca != DATA_PLACE_HOLDER:
    miscc['ask'] = ca
  if cb != DATA_PLACE_HOLDER:
    miscc['bid'] = cb
  return Strike(misc=miscc)


def getPutStrikeInstance(symb, exp, row):
  miscc = {'underlying':symb,
           'strike':getStrike(row),
           'expiration':exp,
           'call':False}
  oi = getPutOpenInt(row)
  ca = getPutAsk(row)
  cb = getPutBid(row)
  if oi != DATA_PLACE_HOLDER:
    miscc['open_int'] = oi
  if ca != DATA_PLACE_HOLDER:
    miscc['ask'] = ca
  if cb != DATA_PLACE_HOLDER:
    miscc['bid'] = cb
  return Strike(misc=miscc)


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
    self.straddles = []
    self.bigger_straddle = False


  def getStraddles(self):
    return self.straddles


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
      self.row.append(DATA_PLACE_HOLDER)
    elif tag == 'td':
      a = getAttr(attrs, 'colspan')
      if a != None:
        a = int(a)
        if a > 10: # a == len(TABLE_HEADERS)
          self.b_expire = True


  def handle_endtag(self, tag):
    if tag == 'table':
      self.begin_table = False
    if tag == 'tr':
      self.begin_row = False
      self.stock_price = False
      if self.begin_table:
        if len(self.row) == len(TABLE_HEADERS):
          call = getCallStrikeInstance(self.symbol,
                                       self.expiration_date,
                                       self.row)
          put = getPutStrikeInstance(self.symbol,
                                     self.expiration_date,
                                     self.row)
          self.data.append(call)
          self.data.append(put)
          if self.bigger_straddle:
            self.bigger_straddle = False
            st = straddle(legs=[call, put], price=self.current_price)
            self.straddles.append(st)
          self.row = []
    if tag == 'td' and self.begin_cell:
      self.begin_cell = False
    if tag == 'td' and self.b_expire:
      self.b_expire = False


  def handle_data(self, data):
    expire_str = 'Expires '
    if self.b_expire and expire_str in data:
      ddd = data[data.find(expire_str) + len(expire_str):]
      self.expiration_date = datetime.datetime.strptime(ddd, "%B %d, %Y")
    if self.begin_cell:
      if self.begin_row:
        ts = data.strip()
        self.row[-1] = ts
      if self.stock_price:
        if 'Current price' not in data:
          self.current_price = float(data)
          ##print '=====', data, '====='
          if len(self.data) > 1:
            st = straddle(legs=[self.data[-1], self.data[-2]],
                          price = self.current_price)
            self.straddles.append(st)
            self.bigger_straddle = True


  def getData(self):
    return self.data


def getOptionMW(symbol='aapl'):
  symb = symbol
  g = GetURL(MATKET_WATCHER_URL % ('stock', symb), encode=True)
  if g == None:
    return
  p = MWFormParser()
  p.feed(g)
  q = MarketWatcherParser()
  q.doXHRtable()
  q.setSymbol(symb)
  for u in p.getLinks():
    g = GetURL('https://www.marketwatch.com' + u)
    if g == None:
      continue
    q.feed(g)
  for i in q.getData():
    print i.getTimeToExp()


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--symbol', default='aapl')
	opts = parser.parse_args()

	getOptionMW(opts.symbol)

 
if __name__ == '__main__':
  main()
