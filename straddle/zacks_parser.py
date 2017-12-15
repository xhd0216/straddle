from HTMLParser import *
import datetime

zacks_api_url = 'https://www.zacks.com/includes/classes/z2_class_calendarfunctions_data.php?calltype=eventscal&date=%s&type=1&search_trigger=0'


# return today's date
def getNowDate():
  now = datetime.datetime.now()
  return datetime.date(now.year, now.month, now.day)    

# give a date (or datetime), return the seconds (of the date, not time)
def getTimeSecond(date):
  try:              
    t = datetime.date(date.year, date.month, date.day)
    r = (t - datetime.date(1970, 1, 1)).total_seconds()
  except:
    return None
  return r

# return the seconds of some days after today
def getDayAfter(days):
  if not isinstance(days, int):
    return None      
  return getTimeSecond(getNowDate() + datetime.timedelta(days=days))

# get a range of days in range(a,b) = [a,b), in seconds.
def getDayAfter(a, b):
  if not isinstance(a, int) or not isinstance(b, int):
    return []                                        
  return [getTimeSecond(getDayAfter(i)) for i in range(a,b)]
  
def GetEarningsInRange(a, b):
  if not isinstance(a, int) or not isinstance(b, int):
    return []
  r = []
  d = getDayAfter(a, b)
  for i in d:
    url = zacks_api_url % str(i)
    # go call the api, it should return a json object
