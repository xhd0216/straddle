"""
  connection to database
"""

import datetime
import logging
import sqlalchemy
from sqlalchemy import orm

from mysql_connect import create_mysql_session
from straddle.market_watcher_parser import getOptionMW
from straddle.strategy import Strike
from db.db_connect import TABLE_NAME, COLUMN_TYPES


# key fields of a strike
KEY_STRIKE_FIELDS = {
  'underlying':'underlying',
  'expiration':'expiration',
  'strike':'strike',
  'is_call':'is_call',
}

SELECT_LATEST = """
  SELECT %s
  FROM
    (
      SELECT underlying, expiration, strike, is_call, max(query_time) AS qt
      FROM %s
      GROUP BY underlying, expiration, strike, is_call
    ) r
  INNER JOIN %s t
  ON t.query_time = r.qt
  AND t.strike=r.strike
  AND t.underlying=r.underlying
  AND t.is_call=r.is_call
  AND t.expiration=r.expiration
  WHERE t.underlying = '%s'
  AND t.strike IN (%s)
  AND t.expiration >= '%s' AND t.expiration <= '%s'
  AND t.is_call IN (%s);
"""

def get_query_latest(table_name, underlying, k_list, exps, call_list):
  if not isinstance(k_list, list):
    k_list = [k_list]
  if not isinstance(exps, list):
    exps = [exps, exps]
  if not isinstance(call_list, list):
    call_list = [call_list]
  select_str = ','.join(['t.'+x for x in COLUMN_TYPES])
  strike_str = ','.join([str(x) for x in k_list])
  call_str = ','.join([str(x) for x in call_list])
  query = SELECT_LATEST % (select_str, table_name, table_name, underlying, strike_str, exps[0], exps[1], call_str)
  return query

query = get_query_latest('test_options', 'spy', [260], ['2018-04-09', '2018-04-18'], True)
print query
conn = create_mysql_session('./test-options.cnf')
res = conn.execute(query)
for r in res:
  print COLUMN_TYPES
  print r
  s = {}
  for i in range(len(COLUMN_TYPES)):
    s[COLUMN_TYPES[i]] = r[i]
  print Strike(s).__json__()
