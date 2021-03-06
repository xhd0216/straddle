import argparse
from HTMLParser import HTMLParser
import os
import sys
import urllib2

from straddle.strategy import *
from util.networks import *
from util.logger import set_logger
from util.misc import fix_instance

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

def getRowLast(row, call):
  return row[1] if call else row[9]


def getRowAsk(row, call):
  return row[5] if call else row[13]


def getRowBid(row, call):
  return row[4] if call else row[12]


def getStrike(row):
  return row[7]


def getRowOpenInt(row, call):
  return row[6] if call else row[14]


def getAttr(attrs, key):
  for x in attrs:
    if key == x[0]:
      return x[1]
  return None

def getStrikeInstance(symb, exp, price, call, row):
  miscc = {'underlying':symb,
           'strike':getStrike(row),
           'expiration':exp,
           'price':price,
           'is_call':call}
  oi = getRowOpenInt(row ,call)
  ca = getRowAsk(row ,call)
  cb = getRowBid(row ,call)
  cl = getRowLast(row ,call)
  if oi != DATA_PLACE_HOLDER and oi != '':
    miscc['open_int'] = oi
  else:
    miscc['open_int'] = 0
  if ca != DATA_PLACE_HOLDER and ca != '':
    miscc['ask'] = ca
  else:
    miscc['ask'] = 0.0
  if cb != DATA_PLACE_HOLDER and cb != '':
    miscc['bid'] = cb
  else:
    miscc['bid'] = 0.0
  if cl != DATA_PLACE_HOLDER and cl != '':
    miscc['last'] = cl
  else:
    miscc['last'] = 0.0
  return create_strike(misc=miscc)


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
    self.last_price = 0.0
    self.last_price_tag = False

  def getLastUnderlyingPrice(self):
    return self.last_price


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
      if a is not None and 'strike-col' in a and 'important' in a:
          self.last_price_tag = True
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
          call = getStrikeInstance(self.symbol,
                                   self.expiration_date,
                                   self.last_price,
                                   True,
                                   self.row)
          put = getStrikeInstance(self.symbol,
                                  self.expiration_date,
                                  self.last_price,
                                  False,
                                  self.row)
          self.data.append(call)
          self.data.append(put)
          if self.bigger_straddle:
            self.bigger_straddle = False
            st = straddle(legs=[call, put], price=self.current_price)
            self.straddles.append(st)
          self.row = []
    if tag == 'td':
      if self.begin_cell:
        self.begin_cell = False
      if self.b_expire:
        self.b_expire = False
      if self.last_price_tag:
        self.last_price_tag = False


  def handle_data(self, data):
    if self.last_price_tag:
      b, a = fix_instance(data, float)
      if not b:
        logging.error('data type error, cannot convert %s to float', data)
      else:
        if a is not None:
          self.last_price = a
        else:
          self.last_price = data
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
          b, a = fix_instance(data, float)
          if not b:
            logging.error('data type error, cannot convert %s to float', data)
          else:
            if a is not None:
              self.current_price = a
            else:
              self.current_price = data
          if len(self.data) > 1:
            st = straddle(legs=[self.data[-1], self.data[-2]],
                          price = self.current_price)
            self.straddles.append(st)
            self.bigger_straddle = True


  def getData(self):
    for r in self.data:
      r.data['price'] = self.getLastUnderlyingPrice()
    return self.data


def getOptionMW(symbol='aapl'):
  g = GetURL(MATKET_WATCHER_URL % ('stock', symbol), encode=True)
  if g == None:
    logging.error('failed to get market watcher page')
    return

  p = MWFormParser()
  p.feed(g)
  q = MarketWatcherParser()
  q.doXHRtable()
  q.setSymbol(symbol)
  for u in p.getLinks():
    g = GetURL('https://www.marketwatch.com' + u)
    if g is None:
      logging.error('failed to get url ', u)
      continue
    q.feed(g)
  return q.getData()


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--symbol', default='aapl')
  parser.add_argument('--log-file', help='log file')
  parser.add_argument('--log-mode', default='a',
                      help='log file mode (a or w)')
  parser.add_argument('--log-level', default='debug',help='log level')

  opts = parser.parse_args()
  if opts.log_file:
    set_logger(level=opts.log_level, filename=opts.log_file,
               mode=opts.log_mode)
  else:
    set_logger(level=opts.log_level, out=sys.stdout)

  #getOptionMW(opts.symbol)


if __name__ == '__main__':
  main()
