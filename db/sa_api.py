"""
  DB APIs
"""
import logging
import sqlalchemy as sa
import os

import db.db_connect as dbc
import straddle.strategy as stg

# global variables
META = sa.MetaData()
OPTIONS_TABLE = sa.Table(
  test_table_name, meta,
  sa.Column('underlying', sa.String(length=10), nullable=False),
  sa.Column('strike', sa.Float, nullable=False),
  sa.Column('expiration', sa.Date, nullable=False),
  sa.Column('price', sa.Float),
  sa.Column('bid', sa.Float),
  sa.Column('ask', sa.Float),
  sa.Column('last', sa.Float),
  sa.Column('open_int', sa.Integer),
  sa.Column('query_time', sa.DateTime),
  sa.Column('is_call', sa.Boolean, nullable=False))


def get_db_link(cnf):
  with open(cnf, 'r') as cobj:
    r = cobj.readlines()
  client_flag = False
  res = {}
  for line in r:
    line = line.strip()
    if line == '':
      continue
    if line[0] == '#':
      # comments
      continue
    if '[client]' in line:
      client_flag = True
    elif '=' not in line:
      if client_flag:
        break
    else:
      a = line.split('=')
      res[a[0].strip()] = a[1].strip()

  if 'host' not in res:
    logging.warning('missing host in cnf file, use localhost')
    res['host'] = 'localhost'
  if 'port' not in res:
    logging.info('no port number in cnf file')
    res['port'] = ''
  else:
    res['port'] = ':' + res['port']
  if 'database' not in res:
    logging.warning('missing database in cnf file')
    res['database'] = ''
  if 'user' not in res:
    logging.warning('missing user in cnf file')
    return 'mysql://%(host)s:%(port)s/%(database)s' % res
  if 'password' not in res:
    logging.warning('missing password in cnf file')
    return None
  if 'driver' not in res:
    logging.warning('default driver: mysql')
    res['driver'] = 'mysql'
  return '%(driver)s://%(user)s:%(password)s@%(host)s%(port)s/%(database)s' % res


def create_sql_engine(dbcnf=None):
  """ create engine """
  if not dbcnf:
    # create empty engine
    return sa.create_engine('sqlite://')
  elif dbcnf[-3:] == '.db':
    # input is db file
    return sa.create_engine('sqlite:///' + dbcnf)
  else:
    # input is config file
    return sa.create_engine(get_db_link(dbcnf))


def create_options_table(engine, test_table_name=dbc.TABLE_NAME):
  """ sqlalchemy create table """
  meta.create_all(engine)
  return OPTIONS_TABLE

#def insert_strike(strk):
#  """ insert strike to options table """
#  assert options_table is not None
#
#  ins = options_table.insert().values(strk.data)
#  engine.execute(ins)
#
#
#def query_options_table():
#  assert options_table is not None
#  que = options_table.select()
#  res = engine.execute(que).fetchall()
#
#  strike_list = []
#  for row in res:
#    # create a dict
#    misc = {}
#    for key in dbc.COLUMN_TYPES:
#      if key in row:
#        misc[key] = row[key]
#      else:
#        logging.warning('missing key %s in strike', key)
#    strk = stg.create_strike(misc)
#    if strk is None:
#      logging.error('failed to create strike from record %s', row)
#    else:
#      strike_list.append(strk)
#
#  return strike_list
