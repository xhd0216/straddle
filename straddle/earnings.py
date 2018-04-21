"""
  yahoo earning parser is not used
"""

import datetime
from lib.objects import objects
from util.misc import isStrUnicode


class earning(objects):
  def __init__(self, misc=None):
    objects.__init__(self)
    self.addField('symbol', str, True)
    # eps is not required, could be '-'
    self.addField('eps', float, False)
    self.addField('date', datetime.datetime, False)

    if isinstance(misc, dict):
      for i in misc.keys():
        self.data[i] = misc[i]

  def setSymbol(self, symbol):
    assert isStrUnicode(symbol)
    self.data['symbol'] = symbol

  def setEPS(self, eps):
    return self.addKey('eps', eps)

  def getSymbol(self):
    return self.getKey('symbol')

  def getEPS(self):
    return self.getKey('EPS')

  def setDate(self, s):
    return self.addKey('date', s)

  def getDate(self):
    return self.getKey('date')
