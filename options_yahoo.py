import json
from HTMLParser import *
from strategy import Strike

s = 'https://finance.yahoo.com/quote/%s/options'

class optionParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.data = []
