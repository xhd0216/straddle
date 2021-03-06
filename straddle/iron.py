"""
  iron condor
"""

import datetime
import logging

from strategy import Strike, strategies, create_strike

class IronCondor(strategies):
  def __init__(self, legs):
    strategies.__init__(self)
    self.data['name'] = 'Iron Condor'
    self.data['legs'] = legs

  @staticmethod
  def create(legs):
    """ create an iron condor strategy """
    assert len(legs) == 4

    for i in range(4):
      if legs[i].getExpirationDate() != legs[0].getExpirationDate():
        logging.error('all legs should have same expiration date')
        return None
    if legs[1].getStrike() - legs[0].getStrike() != legs[3].getStrike() - legs[2].getStrike():
      logging.error('leg spread should be equal')
      return None
    return IronCondor(legs)

  def getTargetReturn(self):
    """ get the target return at expiration """
    legs = self.getStrikes()
    return legs[1].getStrike() - legs[0].getStrike()

  def getBuyPrice(self):
    """ return the price to BUY this strategy """
    """ negative result means creadit """
    a = self.getStrikes()
    return a[0].getAsk() - a[1].getBid() - a[2].getBid() + a[3].getAsk()

  def getSellPrice(self):
    """ return the price to SELL/close this strategy """
    a = self.getStrikes()
    return -a[0].getBid() + a[1].getAsk() + a[2].getAsk() - a[3].getBid()

  def getExpirationDate(self):
    """ get expiration date of the strategy """
    return self.getStrikes()[0].getExpirationDate()


def create_iron_condor(strikes, underlying, expiration, price):
  """ given four strikes prices, return iron condor strategy """
  assert len(strikes) == 4
  misc = dict()
  misc['underlying'] = underlying
  misc['expiration'] = expiration
  misc['price'] = price
  legs = [create_strike(misc = misc, is_call=True, strike=strikes[i]) for i in range(4)]
  return IronCondor.create(legs)

if __name__ == '__main__':
  a = create_iron_condor([23, 25, 27, 29], 'aapl', '2018-04-20', 268.89)
  print a.__json__()
