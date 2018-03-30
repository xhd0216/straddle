import json
from datetime import datetime, date, time

from straddle.strategy import *

def get_json_dict(o):
  assert hasattr(o, "__json__")
  s = o.__json__()
  d = json.loads(s)
  return d

def validate_strike(o):
  assert isinstance(o, Strike)
  d = get_json_dict(o)
  assert d['underlying'] == o.getUnderlying()
  assert d['strike'] == o.getStrike()
  assert d['call'] == o.isCall()
  assert d['expiration'] == o.getExpirationStr()

json1 = '{"strike": 132.5, "underlying": "AAPL", "call": true, "expiration": "Dec 11, 2045"}'

def test_parseStrike():
  r = parseStrike(json1)
  assert r  
  assert r.data
  assert r.getStrike() == 132.5
  assert r.getUnderlying() == "AAPL"
  assert r.isCall()
  assert not r.hasPosition()
  assert r.getExpirationStr() == date(2045, 12, 11).strftime(default_date_format) 
  assert r.getExpirationDate().date() == date(2045, 12, 11)
  validate_strike(r)

json2 = '{"strike": 132.5, "underlying": "AAPL", "call": true, "expiration": "may 11, 2045", "position":200}'

def test_setStrikePosition():
  r = parseStrike(json2)
  assert r.hasPosition()
  r.setPosition(60)
  assert r.getPosition() == 260
  r.setPosition(-320)
  assert r.getPosition() == -60
  assert r.hasPosition()
  r.setPosition(560, False)
  assert r.getPosition() == 560
  r.setPosition(-100, False)
  assert r.getPosition() == -100
  r.setPosition(340)
  assert r.getPosition() == 240
  assert r.hasPosition()
  r.setPosition(0, False) 
  ## even if position is 0
  assert r.hasPosition()
  assert r.isValid()
  assert r.error == None
  
def test_getStrategyName():
  strike1 = Strike(underlying='aapl', strike=50.0, expiration="Dec 17, 2017", call=True)
  strike2 = Strike(underlying='aapl', strike=50.0, expiration="Dec 17, 2017", call=False) 
  assert strike1.setAsk(3.14)
  assert strike2.setAsk(4.21) 
  s = straddle(legs=[strike1, strike2], price=52.35)
  assert s.getName() == "straddle"
  d = get_json_dict(s)
  assert d['name'] == "straddle"
  assert s.isValid()
  assert s.getStraddlePrice() == 7.35 
