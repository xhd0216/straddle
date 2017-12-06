import os
import json
import urllib2
from HTMLParser import *
import datetime, time
from straddle.objects import objects
from config.url_config import URLDB
from straddle.earnings import *

option_date_format = '%B %d, %Y'
starting_page = 'https://finance.yahoo.com/quote/%s/options?straddle=true'

def find_matching(s, b, forward=True):
  if forward:
    if b == '{':
      c = '}'
    elif b == '[':
      c = ']'
    elif b == '(':
      c = ')'
    else:
      return -1
  else:
    return -1
  """
  else:
    if b == '}':
      c = '{'
    elif b == '}':
      c = '['
    elif b == ')':
      c = '('
  """
  i = s.find(b) + 1
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
  def hasAttr(self, attrs, key):
    for x in attrs:
      if key == x[0]:
        return x[1]
    return None
def GetOptionChainPage():
  udb = URLDB()
  earning_url = udb.getItem('earning')
  options_url = udb.getItem('options')
  if url == None:
    print 'failed to get url for earning'
    return 
  try:
    f = urllib2.urlopen(earning_url)
    g = f.read()
    f.close()
  except:
    print 'failed to open page'
    return
  p = earningParser()
  p.feed(g)
  for i in p.data:
    # assert isinstance(i, earning)
    u = options_url % i.getSymbol()
    f = urllib2.urlopen(u)
    if f == None:
      print 'failed to open ', u
    g = f.read()
    # place a parser here
  return
    
    
def getOptionJson():
  f = urllib2.urlopen(starting_page % 'DE')
  print f.getcode()
  g = f.read()
  f.close()

  r=g.find('root.App.main')
  g1 = g[r:]
  left = g1.find('{')
  g1 = g1[left:]
  right = find_matching(g1, '{')
  j = json.loads(g1[:right+1])
  print_struct(j, '')
