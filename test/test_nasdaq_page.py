from straddle.nasdaq_parser import *
import os
"""
def test_option_page():
  f = open(os.path.join(os.path.dirname(__file__), 'nasdaq_option_chain.html'))
  g = f.read()
  f.close()
  p = nasdaqParser()
  p.feed(g)

  for i in p.getData():
    miscc = {'underlying':symbol, 'strike':i[8], 'expiration':i[0], 'call':True, 'open_int':i[6]}
    if i[3] != '-':
      miscc['bid'] = i[3]
    if i[4] != '-':
      miscc['ask'] = i[4]
    call = Strike(misc=miscc)
    r.append(call)
    miscp = {'underlying':symbol, 'strike':i[8], 'expiration':i[9], 'call':False, 'open_int':i[15]}
    if i[12] != '-':
      miscp['bid'] = i[12]
    if i[13] != '-':
      miscp['ask'] = i[13]
    put = Strike(misc=miscp)
    r.append(put)
def test_nasdaq_json():
  p = nasdaqParser()
  p.data = [[1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6]]
  assert p.__json__() == '{\"data\":[{\"one\":1,\"two\":2,\"three\":3},{\"one\":4,\"two\":5,\"three\":6}]}'
"""
