"""
  connection to database
"""
import argparse
import datetime
import logging
import sqlalchemy
from sqlalchemy import *
import sys

from mysql_connect import create_mysql_session
from straddle.strategy import Strike
from util.logger import set_logger






TABLE_NAME = 'test_options'
COLUMN_TYPES = ['underlying',
                'price',
                'strike',
                'expiration',
                'is_call',
                'query_time',
                'ask',
                'bid',
                'last',
                'open_int']


def create_test_options_table(engine, test_table_name=TABLE_NAME):
  """ sqlalchemy create table """
  metadata = MetaData()
  share_table = Table(test_table_name, metadata,
                      Column('underlying', String(length=10), nullable=False),
                      Column('strike', Float, nullable=False),
                      Column('expiration', Date, nullable=False),
                      Column('price', Float),
                      Column('bid', Float),
                      Column('ask', Float),
                      Column('last', Float),
                      Column('open_int', Integer),
                      Column('query_time', DateTime),
                      Column('is_call', Boolean, nullable=False))
  metadata.create_all(engine)


def obj_convert(o):
  """ convert objects to sql str """
  # note: isinstance(datetime.datetime, datetime.date) = True
  # note: isinstance(datetime.date, datetime.datetime) = False
  if isinstance(o, datetime.datetime):
    if o.hour == 0 and o.minute == 0:
      # this is also a date, only print date
      return '"%s"' % datetime.datetime.strftime(o, '%Y-%m-%d')
    else:
      return '"%s"' % datetime.datetime.strftime(o, '%Y-%m-%d %H:%M:%S')
  elif isinstance(o, datetime.date):
    return '"%s"' % datetime.date.strftime(o, '%Y-%m-%d')
  elif isinstance(o, str) or isinstance(o, unicode):
    return '"%s"' % o
  else:
    # int, bool, float, etc
    return str(o)


INSERT_SQL = """
  INSERT IGNORE INTO %s (%s) VALUES (%s);
"""

def create_values_str(strike):
  """ create values str used in sql """
  data = strike.data
  res = []
  for cv in COLUMN_TYPES:
    if cv in data:
      res.append(cv)
  cols = ','.join(res)
  vals = ','.join([obj_convert(data[x]) for x in res])
  if 'query_time' not in data:
    # query time is not a required field in strike,
    # but it is a primary key in db
    cols += ',query_time'
    vals += ',' + obj_convert(datetime.datetime.now())
  return cols, vals


def create_insert_sql(strike, table_name=TABLE_NAME):
  """ create sql insert statement for a strike """
  cols, vals = create_values_str(strike)
  return INSERT_SQL % (table_name, cols, vals)


def insert_multiple(session, arr):
  """ insert an array of strikes to database """
  if not arr:
    return
  assert isinstance(arr[0], Strike)
  cmds = []
  for s in arr:
    if not s.isValid():
      logging.error('strike is not valid')
      continue
    cmd = create_insert_sql(s)
    cmds.append(cmd)
  session.execute_multiple(cmds)
