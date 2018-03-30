import os

from straddle.market_watcher_parser import *


def test_empty_page():
  f = open(os.path.join(os.path.dirname(__file__), 'market_watch_empty.html'))
  g = f.read()
  f.close()
  p = MWFormParser()
  p.feed(g)
  assert len(p.getLinks()) == 0
