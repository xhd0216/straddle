from straddle.nasdaq_parser import *
import os

def test_option_page():
  f = open(os.path.join(os.path.dirname(__file__), 'yahoo_option_page.html'))
  g = f.read()
  f.close()
  p = nasdapParser()
  p.feed(g)

def test_nasdaq_json():
  p = nasdaqParser()
  p.data = [[1,2,3],[4,5,6]]
  p.header_names=['one','two','three']
  assert p.__json__() == '{\"data\":[{\"one\":1,\"two\":2,\"three\":3},{\"one\":4,\"two\":5,\"three\":6}]}'
