import os
from straddle.insider_parser import *

def test_insider_page():
  f = open(os.path.join(os.path.dirname(__file__), 'insider.html'))
  g = f.read()
  f.close()
  p = insiderParser()
  p.feed(g) 
  print p.getTable()
  t = p.getAggregatedTable()
  for i in t.keys():
    print i, 'value:', t[i][1], 'shares:', t[i][0]
