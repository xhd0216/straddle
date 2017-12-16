"""
deprecated

parse yahoo option page
"""


import sys
import os
import json
from HTMLParser import *
import datetime, time
from objects import objects
from config.url_config import URLDB
from earnings import *

option_date_format = '%B %d, %Y'
starting_page = 'https://finance.yahoo.com/quote/%s/options?straddle=true'

def find_matching(s, b, forward=True):
  if b == '{':
    c = '}'
  elif b == '[':
    c = ']'
  elif b == '(':
    c = ')'
  else:
    return -1
  i = s.find(b) + 1
  if i == 0:
    # cannot find {
    return -1
  n = 1
  while i < len(s):
    if s[i] == b:
      n += 1
    elif s[i] == c:
      n -= 1
    if n == 0:
      return i
    i += 1
  return -1

def print_struct(js, key, prefix=''):
  if not isinstance(js, dict):
    return
  for i in js.keys():
    ps = prefix + '/' + i
    print ps
    print_struct(js[i], key, ps)

def date_to_second(s, fm=option_date_format):
  try:
    d = datatime.datetime.strptime(s, fm)
    r = time.mktime(d.timetuple())
  except:
    print 'fail to convert time'
    return None
  return r

class optionParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.expd = False
    self.item = []
    self.data = []
  def getAttr(self, attrs, key):
    for x in attrs:
      if key == x[0]:
        return x[1]
    return None
  def handle_starttag(self, tag, attrs):
    if tag == 'select':
      print attrs
      a = self.getAttr(attrs, 'class')
      if a != None and a == 'Fz(s)':
        self.expd = True
    if tag == 'option' and self.expd:
      b = self.getAttr(attr, 'value')
      if b != None:
        print b
  def handle_data(self, data):
    if self.expd:
      print data
  def hadnle_endtag(self, tag):
    if tag == 'select' and self.expd:
      self.expd = False
def getOptionJson(symbol):
  g = GetURL(starting_page % symbol)
  r=g.find('root.App.main')
  g1 = g[r:]
  left = g1.find('{')
  g1 = g1[left:]
  right = find_matching(g1, '{')
  j = json.loads(g1[:right+1])
  #print json.dumps(j, indent=3)
  #print_struct(j, '')
def GetOptionChainPage():
  udb = URLDB()
  earning_url = udb.getItem('earning').getURL()
  options_url = udb.getItem('options').getURL()
  #print earning_url
  #print options_url
  if earning_url == None:
    print 'failed to get url for earning'
    return 
  try:
    g = GetURL(earning_url)
  except:
    print 'failed to open page'
    return
  p = earningParser()
  p.feed(g)
  for i in p.data:
    # assert isinstance(i, earning)
    u = options_url % i.getSymbol()
    # print u
    # getOptionJson(i.getSymbol())
    k = GetURL(u)
    o = optionParser()
    o.feed(k)
  return
#GetOptionChainPage() 
