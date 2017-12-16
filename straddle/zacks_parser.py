from HTMLParser import *
from util.misc import *
from util.networks import *
from straddle.earnings import *
import json


zacks_heading = ['symbol', 'company', 'market-cap', 'time', 'estimate', 'reported', 'surprise', 'surprise-percent', 'price-change', 'report-camera']
zacks_api_url = 'https://www.zacks.com/includes/classes/z2_class_calendarfunctions_data.php?calltype=eventscal&date=%s&type=1&search_trigger=0'

def GetEarningsInRange(a, b):
  if not isinstance(a, int) or not isinstance(b, int):
    return []
  r = []
  d = getDayAfterRange(a, b)
  for t in d:
    url = zacks_api_url % str(getTimeSecond(t))
    print url
    g = GetURL(url)
    j = json.loads(g)
    for i in j['data']:
      # get symbol
      s = i[0]
      index = s.find('rel=')
      if index == -1:
        print 'error loading symbol'
        continue
      begin = s[index + 5:]
      end = begin.find('\"')
      symbol = begin[:end]
      # print symbol
      # get eps
      e = i[4]
      # print e
      earn = earning()
      earn.setSymbol(symbol)
      #print earn.data['symbol']
      earn.setEPS(e)
      earn.setDate(str(t))
      print earn.__json__()
    # print json.dumps(j, indent=3)
    # go call the api, it should return a json object
GetEarningsInRange(3,6)
