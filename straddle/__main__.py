from straddle.earnings import *
from straddle.market_watcher_parser import *
import os
import sys, getopt

print "welcome to straddle"


def getAllEarnings():
  g = (yahoo_earning_url)
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
    print "========================"
    print d.data
    getOptionMW(u) 
 
if __name__=="__main__":
  try:
    opts, args = getopt.getopt(sys.argv[1:],"has:",["symbol="])
  except getopt.GetoptError:
    print 'python straddle [arguments]'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'python straddle [argument]'
    elif opt == '-a':
      getAllEarnings()
    elif opt == '-s':
      getOptionMW(arg)
