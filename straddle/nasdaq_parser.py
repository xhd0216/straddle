from HTMLParser import *
from straddle.strategy import *
import urllib2

s = 'http://www.nasdaq.com/symbol/%s/option-chain'
headers = ["Calls", "Last", " Chg", "Bid", "Ask", "Vol", "OpenInt", "Root", "Strike", "Puts", "Last", "Chg", "Bid", "Ask", "Vol", "OpenInt"]
n = len(headers)


class nasdaqParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.seen_th = False
    self.row_begin = False
    self.entry = None
    self.seen_table = False
    self.counter = 0
    self.table = False
    self.td = False
    self.data = []
    self.call = None
  def handle_starttag(self, tag, attrs):
    if tag == 'table':
      self.table = True
    if tag == 'th':
      self.seen_th = True
    if tag == 'tr' and self.seen_table:
      self.counter = -1
      self.row_begin = True
      if self.seen_table:
        self.entry = ['-']*n
    if tag == 'td':
      self.td = True
      self.counter += 1
  def handle_endtag(self, tag):
    if tag == 'table':
      self.table = False
      self.seen_table = False
    if tag == 'th':
      self.seen_th = False
    if tag == 'tr':
      self.row_begin = False
      #print self.entry
      if self.entry != None:
        self.data.append(self.entry)
    if tag == 'td':
      self.td = False
  def handle_data(self, data):
    if self.seen_th:
      h = data.split()
      if len(h) > 1:
        return
      if 'Root' in h:
        # determine if this is the right table we are looking for
        self.seen_table = True
    if self.row_begin and self.seen_table:
      if self.td:
        self.entry[self.counter] = data
  def __json__(self):
    js = '{\"data\":['
    for t in range(len(self.data)):
      i = self.data[t]
      js += '{' 
      for j in range(len(i)):
        js += '\"' + headers[j] + '\":' + '\"' + str(i[j]) + '\"'
        if j != len(i) - 1:
          js += ','
      js += '}'
      if t != len(self.data) - 1:
        js += ','
    js += ']}'
    return js
  def getData(self):
    return self.data
def get_strike_list(symbol):
  f = urllib2.urlopen(s % symbol)
  g = f.read()
  f.close()
  r = []
  p = nasdaqParser()
  p.feed(g)    
  for i in p.getData():
    miscc = {'underlying':symbol, 'strike':i[8], 'expiration':i[0], 'call':True, 'open_int':i[6]}
    if i[3] != '-':
      miscc['bid'] = i[3]
    if i[4] != '-':
      miscc['ask'] = i[4]
    call = Strike(misc=miscc)
    r.append(call)
    miscp = {'underlying':symbol, 'strike':i[8], 'expiration':i[9], 'call':False, 'open_int':i[15]}
    if i[12] != '-':
      miscp['bid'] = i[12]
    if i[13] != '-':
      miscp['ask'] = i[13]
    put = Strike(misc=miscp)
    r.append(put)
  return r
