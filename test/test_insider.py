import urllib2
import os
from lib.parser import *

## columns in the title
columns = ['symbol', 'issuer', 'insider name', 'shares', 'price', 'value', 'date']

class insiderParser(myParser):
  def __init__(self):
    myParser.__init__(self)
    self.data_row = []
    self.table = []
    self.has_data = False
    self.last_symbol = ''
  def handle_starttag(self, tag, attrs):
    self.tagOn(tag)
    if tag == 'td':
      self.has_data = False
  def handle_data(self, data):
    self.has_data = True
    if self.isTagOn('table') and self.isTagOn('tr') and self.isTagOn('td'):
      if len(data) > 0: ## non-empty data
        self.data_row.append(data)
        if len(self.data_row) == 1:
          self.last_symbol = data 
  def handle_endtag(self, tag):
    if tag == 'td' and self.has_data == False:
      self.data_row.append(self.last_symbol)
    if tag == 'tr':
      if self.isTagOn('table'):
        print self.data_row
        self.table.append(self.data_row)
        self.data_row = []
    self.tagOff(tag)

def test_insider_page():
  ## s = 'http://www.insider-monitor.com/top10_insider_buys_week.html'
  f = open(os.path.join(os.path.dirname(__file__), 'insider.html')
  g = f.read()
  f.close()
  p = insiderParser()
  p.feed(g)
