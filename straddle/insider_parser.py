from lib.parser import myParser
from util.misc import *

## s = 'http://www.insider-monitor.com/top10_insider_buys_week.html'
## columns in the title
columns = ['symbol', 'issuer', 'insider name', 'shares', 'price', 'value', 'date']
num_columns = len(columns)

class insiderParser(myParser):
  def __init__(self):
    myParser.__init__(self)
    self.data_row = []
    self.table = []
    self.has_data = False
    self.last_symbol = ''
    self.aggregated = dict()

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
    if tag == 'td' and not self.has_data:
      self.data_row.append(self.last_symbol)
    if tag == 'tr':
      if self.isTagOn('table'):
        if len(self.data_row) >= num_columns:
          self.table.append(self.data_row)
        self.data_row = []
    self.tagOff(tag)

  def getTable(self):
    return self.table

  def getAggregatedTable(self):
    #sym = ''
    #total_value = 0
    #total_shares = 0
    for i in self.table:
      sym = i[0]
      if sym not in self.aggregated:
        self.aggregated[sym] = [0, 0]
      d = self.aggregated[sym]
      d_s = i[3]
      d_v = i[5]
      b_s, a_s = fix_instance(d_s, int)
      b_v, a_v = fix_instance(d_v, int)
      if not b_s or not b_v:
        continue
      if a_s != None:
        d_s = a_s
      if a_v != None:
        d_v = a_v
      d[0] += d_s
      d[1] += d_v
    return self.aggregated
