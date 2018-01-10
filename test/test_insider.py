import urllib2
from lib.parser import *

columns = ['symbol', 'issuer', 'insider name', 'shares', 'price', 'value', 'date']

class insiderParser(myParser):
  def __init__(self):
    myParser.__init__(self)
    self.data_row = []
    self.has_data = False
    self.last_symbol = ''
  def handle_starttag(self, tag, attrs):
    self.tagOn(tag)
    if tag == 'td':
      self.has_data = False
  def handle_data(self, data):
    self.has_data = True
    if self.isTagOn('table') and self.isTagOn('tr') and self.isTagOn('td'):
      self.data_row.append(data)
      if len(self.data_row) == 1:
        self.last_symbol = data 
  def handle_endtag(self, tag):
    if tag == 'td' and self.has_data == False:
      self.data_row.append(self.last_symbol)
    if tag == 'tr':
      if self.isTagOn('table'):
        print self.data_row
        self.data_row = []
    self.tagOff(tag)

s = 'http://www.insider-monitor.com/top10_insider_buys_week.html'
f = urllib2.urlopen(s)
g = f.read()
p = insiderParser()
p.feed(g)
