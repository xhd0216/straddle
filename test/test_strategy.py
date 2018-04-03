import json
from datetime import datetime, date, time

from straddle.strategy import *

def get_json_dict(o):
  assert hasattr(o, "__json__")
  s = o.__json__()
  print s
  d = json.loads(s)
  return d

def validate_strike(o):
  assert isinstance(o, Strike)
  d = get_json_dict(o)
  assert d['underlying'] == o.getUnderlying()
  assert d['strike'] == o.getStrike()
  assert d['call'] == o.isCall()
  assert d['expiration'] == o.getExpirationStr(format_str='%Y-%m-%d')

json1 = '{"strike": 132.5, "underlying": "AAPL", "call": true, "expiration": "Dec 11, 2045", "price": 128.31}'

def test_parseStrike():
  r = parse_strike(json1)
  assert r  
  assert r.data
  assert r.getStrike() == 132.5
  assert r.getUnderlying() == "AAPL"
  assert r.isCall()
  print r.getExpirationStr()
  assert r.getExpirationStr() == date(2045, 12, 11).strftime(default_date_format) 
  assert r.getExpirationDate().date() == date(2045, 12, 11)
  validate_strike(r)

json2 = '{"strike": 132.5, "underlying": "AAPL", "call": true, "expiration": "may 11, 2045", "price": 128.35, "position":200}'

def test_getStrategyName():
  strike1 = create_strike(None, underlying='aapl', strike=50.0, expiration=datetime.datetime.strptime("Dec 17, 2017", "%b %d, %Y"), call=True, price=57.21)
  strike2 = create_strike(None, underlying='aapl', strike=50.0, expiration=datetime.datetime.strptime("Dec 17, 2017", "%b %d, %Y"), call=False, price=57.21) 
  assert strike1.setAsk(3.14)
  assert strike2.setAsk(4.21)
  s = straddle(legs=[strike1, strike2], price=52.35)
  assert s.getName() == "straddle"
  d = get_json_dict(s)
  assert d['name'] == "straddle"
  assert s.isValid()
  assert s.getStraddlePrice() == 7.35 
