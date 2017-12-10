from HTMLParser import *
import urllib2

s = 'http://www.nasdaq.com/symbol/%s/option-chain'

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
  def handle_starttag(self, tag, attrs):
    if tag == 'table':
      self.counter = 0
      self.headers = []
      self.table = True
    if tag == 'th':
      self.seen_th = True
      self.counter += 1
    if tag == 'tr' and self.seen_table:
      self.counter = 0
      self.row_begin = True
      self.entry = []
    if tag == 'td':
      self.td = True
      self.counter += 1
  def handle_endtag(self, tag):
    if tag == 'table':
      print 'headers', self.headers
      self.table = False
    if tag == 'th':
      self.seen_th = False
    if tag == 'tr':
      self.row_begin = False
      #print self.entry
      self.data.append(self.entry)
    if tag == 'table':
      self.seen_table = False
    if tag == 'td':
      self.td = False
  def handle_data(self, data):
    if self.seen_th:
      if 'Root' in data:
        self.seen_table = True
      if 'Puts' in data:
        self.headers.append(self.counter)
        self.header_names.append('puts')
      elif 'Calls' in data:
        self.headers.append(self.counter)
        self.header_names.append('calls')
      elif 'Bid' in data:
        self.headers.append(self.counter)
        self.header_names.append('bid')
      elif 'Ask' in data:
        self.headers.append(self.counter)
        self.header_names.append('ask')
      elif 'Strike' in data:
        self.headers.append(self.counter)
        self.header_names.append(strike)
    if self.row_begin:
      if self.counter in self.headers and self.td:
        ##print self.counter, data
        self.entry.append(data)
  def __json__(self):
    js = '{\"data\":['
    for t in range(len(self.data)):
      i = self.data(t)
      js += '{' 
      for j in range(len(i)):
        js += '\"' + self.header_names[j] + '\":' + str(i[j])
        if j != len(i) - 1:
          js += ','
      js += '}'
      if t != len(self.data) - 1:
        js += ','
    js += ']}'
    return js
"""
f = urllib2.urlopen(s % 'de')
g = f.read()
f.close()

p = nasdaqParser()
p.feed(g)    
"""
