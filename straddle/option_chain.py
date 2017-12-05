import os
import json
import urllib2
import HTMLParser
import datetime, time
from straddle.objects import objects
from config.url_config import URLDB
from straddle.earnings import *

option_date_format = '%B %d, %Y'

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
    
    
