from HTMLParser import *
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
    self.headers = []
    self.header_names = []
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
        self.seen_table = True
      """
      if 'Puts' in h:
        self.headers.append(self.counter)
        self.header_names.append('puts')
        self.call = False
      elif 'Calls' in h:
        self.headers.append(self.counter)
        self.header_names.append('calls')
        self.call = True
      elif 'Bid' in h:
        self.headers.append(self.counter)
        if self.call:
          self.header_names.append('call_bid')
        else:
          self.header_names.append('put_bid')
      elif 'Ask' in h:
        self.headers.append(self.counter)
        if self.call:
          self.header_names.append('call_ask')
        else:
          self.header_names.append('put_ask')
      elif 'Strike' in h:
        self.headers.append(self.counter)
        self.header_names.append('strike')
      """
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
f = urllib2.urlopen(s % 'de')
g = f.read()
f.close()

p = nasdaqParser()
p.feed(g)    
print p.data
print p.__json__()
