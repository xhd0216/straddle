import os
import json
import urllib2
from straddle.objects import objects
from config.url_config import URLDB
from straddle.earnings import *

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
    
    
