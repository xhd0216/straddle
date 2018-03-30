"""
  strangle
"""

import datetime
import logging

from lib.objects import objects
from util.misc import *
from strategy import Strike, strategies

class Strangle(strategies):
  def __init__(self, legs, price=None):
    strategies.__init__(self)
    self.data['name'] = 'Strangle'
    self.data['strikes'] = legs
    if price != None:
      self.data['underlying_price'] = price

  @classmethod
  def create_strangle(legs, price):
    """ create an iron condor strategy """
    if len(legs) != 2:
      logging.error('strangle should have 2 legs')
      return None
    if legs[1].getExpirationDate() != self.getExpirationDate():
      logging.error('all legs should have same expiration date')
      return None
    
    if not legs[0].isCall() or not legs[1].isCall():
      logging.error('Strangle legs must be calls')
      return None
    return Strangle(legs, price)
  
  def getBuyPrice(self):
    """ return the price to BUY this strategy """
    legs = self.getStrikes()
    return legs[0].getAsk() + legs[1].getAsk()

  def getSellPrice(self):
    """ return the price to SELL this strategy """
    legs = self.getStrikes()
    return legs[0].getBid() + legs[1].getBid()

  def getExpirationDate(self):
    """ get expiration date of the strategy """
    return self.getStrikes()[0].getExpirationDate()
