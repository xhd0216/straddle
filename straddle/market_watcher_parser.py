import HTMLParser

## example: index/vix, stock/aapl
market_watcher_url = 'https://www.marketwatch.com/investing/%s/%s/options'

table_headings=["Symbol", "Last", "Change", "Vol", "Bid", "Ask", "OpenInt", "Strike", "Symbol", "Last", "Change", "Vol", "Bid", "Ask", "OpenInt"]
def MarketWatcherParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.begin_table = False
    self.begin_row = False
    self.stock_price = False
    self.row = []
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
        self.stock_price = True
  def handle_endtag(self, tag):
    if tag == 'table':
      self.begin_table = False
    if tag = 'tr':
      self.begin_row = False
      self.stock_price = False
      if self.begin_table:
        print self.row
  def handle_data(self, data):
    if self.begin_row:
      self.row.append(data)
    if self.stock_price:
      if 'Current price' not in data:
        print '=====', data, '====='
  def getAttr(self, attrs, key):
    for x in attrs:
      if key == x[0]:
        return x[1]
    return None
