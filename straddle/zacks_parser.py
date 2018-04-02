"""
  get earning calendar from zacks
"""

from HTMLParser import *
import json
import logging

from util.misc import *
from util.networks import GetURL
from straddle.earnings import earning


ZACKS_HEADING = ['symbol', 'company', 'market-cap', 'time', 'estimate', 'reported', 'surprise', 'surprise-percent', 'price-change', 'report-camera']
ZACKS_API_URL = 'https://www.zacks.com/includes/classes/z2_class_calendarfunctions_data.php?calltype=eventscal&date=%s&type=1&search_trigger=0'

def GetEarningsInRange(a, b):
  """ get earning calendar """
  res = []
  date_array = getDayAfterRange(a, b)
  for t in date_array:
    url = ZACKS_API_URL % str(getTimeSecond(t))
    g = GetURL(url)
    if g is None:
      logging.error("failed to date %s, url=%s", datetime.datetime.strftime(t, '%Y-%m-%d'), url)
      # failed to load page
      continue
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
      # get eps
      e = i[4]
      # print e
      earn = earning()
      earn.setSymbol(symbol)
      earn.setEPS(e)
      earn.setDate(str(t))
      res.append(earn)
  return res


def main():
  logging.info("in zacks")
  for earning in GetEarningsInRange(3,6):
    print earning.__json__()


if __name__ == '__main__':
  main()
