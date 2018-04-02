import datetime
import logging
import sqlalchemy

from mysql_connect import get_mysql_connect

def get_engine(cnf):
  return sqlalchemy.create_engine(get_mysql_connect(cnf))

def insert_options():
  rows = sqlalchemy.Table('options_test')
  i = rows.insert()
  i.execute({'underlying':'aapl', 'strike':160, 'expiration':'2018-04-20', 'is_call':True, 'query_time':datetime.datetime.now()})

