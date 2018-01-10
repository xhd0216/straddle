from HTMLParser import *
##from objects import objects
##from urllib2 import *
import urllib2

class myParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.tags = dict()
  def hasAttrs(self, attrs, key):
    for x in attrs:
      if key == x[0]:
        return True, x[1]
    return False, None
  def tagOn(self, tag):
    ## self.tags[tag] is a stack
    if tag not in self.tags:
      self.tags[tag] = 0
    self.tags[tag] += 1
  def tagOff(self, tag):
    if tag not in self.tags:
      ## encounter an end tag before a start tag, error
      ## give a warning, this is an html issue, don't handle
      self.tags[tag] = 1
    self.tags[tag] -= 1
  def isTagOn(self, tag):
    if tag not in self.tags:
      return False
    return self.tags[tag] > 0
  def handle_starttag(self, tag, attrs):
    self.tagOn(tag)
  def handle_endtag(self, tag):
    self.tagOff(tag)

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
