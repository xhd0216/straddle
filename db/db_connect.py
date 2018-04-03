import datetime
import logging
import sqlalchemy

from mysql_connect import get_mysql_connect
from straddle.market_watcher_parser import getOptionMW
from straddle.strategy import Strike


TABLE_NAME = 'test_options'
COLUMN_TYPES = ['underlying',
                'price',
                'strike',
                'expiration',
                'call',
                'query_time',
                'ask',
                'bid',
                'last',
                'open_int']

def obj_convert(o):
  """ convert objects to sql str """
  if isinstance(o, datetime.date):
    return '"%s"' % datetime.date.strftime(o, '%Y-%m-%d')
  elif isinstance(o, datetime.datetime):
    if o.hour == 0 and o.minute == 0:
      # only print date
      return '"%s"' % datetime.datetime.strftime(o, '%Y-%m-%d')
    else:
      return '"%s"' % datetime.datetime.strftime(o, '%Y-%m-%d %H:%M:%S')
  elif isinstance(o, str) or isinstance(o, unicode):
    return '"%s"' % o
  else:
    # int, bool, float, etc
    return str(o)

def get_engine(cnf):
  return sqlalchemy.create_engine(get_mysql_connect(cnf))


INSERT_SQL = """
  insert into %s (%s) values (%s);
"""

def create_values_str(strike):
  data = strike.data
  res = []
  for cv in COLUMN_TYPES:
    if cv in data:
      res.append(cv)
  cols = ','.join(res)
  vals = ','.join([obj_convert(data[x]) for x in res])
  return cols, vals


def create_insert_sql(strike, table_name=TABLE_NAME):
  cols, vals = create_values_str(strike)
  return INSERT_SQL % (table_name, cols, vals)


def insert_multiple(eng, arr):
  if not arr:
    return
  assert isinstance(arr[0], Strike)
  Session = sqlalchemy.orm.sessionmaker(bind=engine.engine)
  session = Session()
  try:
    for s in arr:
      cmd = sqlalchemy.text(create_insert_sql(s))
      session.execute(cmd)
    session.commit()
  except:
    logging.error('failed to insert strike to database')
    session.rollback()
  finally:
    session.close()


if __name__ == '__main__':
  row = getOptionMW()
  #eng = sqlalchemy.create_engine('mysql://localhost/test_vdb')
  #insert_multiple(eng, row[:10])
  for i in range(10):
    print create_insert_sql(row[i])

