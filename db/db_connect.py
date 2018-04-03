import datetime
import logging
import sqlalchemy

from mysql_connect import get_mysql_connect
from straddle.market_watcher_parser import getOptionMW
from straddle.strategy import Strike

def get_engine(cnf):
  return sqlalchemy.create_engine(get_mysql_connect(cnf))

COLUMNS = ['underlying', 'price', 'strike', 'expiration', 'call', 'query_time', 'ask', 'bid', 'last', 'open_int']

def insert_options(eng, s):
  assert isinstance(s, Strike)
  rows = sqlalchemy.Table('options_test')

  i = rows.insert()
  i.execute(s.data())
  #i.execute({'underlying':'aapl', 'price':152.31, 'strike':160, 'expiration':'2018-04-20', 'is_call':True, 'query_time':datetime.datetime.now()})


if __name__ == '__main__':
  row = getOptionMW()[0]
  insert_options(row)

