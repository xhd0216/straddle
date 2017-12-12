from HTMLParser import HTMLParser
import urllib2
## example: index/vix, stock/aapl, fund/dust
market_watcher_url = 'https://www.marketwatch.com/investing/%s/%s/options'

table_headings=["Symbol", "Last", "Change", "Vol", "Bid", "Ask", "OpenInt", "Strike", "Symbol", "Last", "Change", "Vol", "Bid", "Ask", "OpenInt"]
class MarketWatcherParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.begin_table = False
    self.begin_row = False
    self.stock_price = False
    self.row = []
    self.begin_cell = False
    self.expiration_date = False
  def handle_starttag(self, tag, attrs):
    if tag == 'table':
      a = self.getAttrs(attrs, 'class')
      if a != None and 'optiontable' in a:
        self.begin_table = True
    elif tag == 'tr' and self.begin_table:
      a = self.getAttrs(attrs, 'class')
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
      a = self.getAttrs(attrs, 'class')
      if 'acenter' not in a:
        self.begin_cell = True
      self.row.append('-')
    elif tag == 'td':
      a = self.getAttrs(attrs, 'colspan')
      if a != None:
        a = int(a)
        if a > 10: # a == len(table_headings)
          self.expiration_date = True
  def handle_endtag(self, tag):
    if tag == 'table':
      self.begin_table = False
    if tag == 'tr':
      self.begin_row = False
      self.stock_price = False
      if self.begin_table:
        if len(self.row) == len(table_headings):
          print self.row
          self.row = []
    if tag == 'td' and self.begin_cell:
      self.begin_cell = False
    if tag == 'td' and self.expiration_date:
      self.expiration_date = False
  def handle_data(self, data):
    expire_str = 'Expires '
    if self.expiration_date and expire_str in data:
      print "*****", data[data.find(expire_str) + len(expire_str):], "*****"
    if self.begin_cell:
      if self.begin_row:
        ts = data.strip()
        self.row[-1] = ts
      if self.stock_price:
        if 'Current price' not in data:
          print '=====', data, '====='
  def getAttrs(self, attrs, key):
    for x in attrs:
      if key == x[0]:
        return x[1]
    return None

def getOptionMW()
  f = urllib2.urlopen(market_watcher_url % ('stock', 'aapl'))
  print f.getcode()
  g = f.read()
  f.close()
  p = MarketWatcherParser()
  p.feed(g)
