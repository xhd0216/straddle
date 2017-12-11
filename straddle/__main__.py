from straddle.earnings import *
from straddle.nasdaq_parser import *
import os
import urllib2

print "welcome to straddle"

#yahoo_earning_page = 'https://finance.yahoo.com/calendar/earnings'

def getAllEarnings():
  f = urllib2.urlopen(yahoo_earning_url)
  if f.getcode() != 200:
    print 'cannot open file %s' % yahoo_earning_url
    f.close()
    return
  g = f.read()
  f.close()
  ep = earningParser()
  ep.feed(g)
  data = ep.getData()
  if len(data) == 0:
    print "no ER today"
    return
  for d in data:
    # d: earning
    # r: list of Strikes
    # u: symbol
    u = d.getSymbol()
    r = get_strike_list(u)
    print "========================"
    print d.data
    for st in r:
      print st.__json__()
      
  
getAllEarnings()
