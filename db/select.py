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
  """ get latest strikes for given condition """
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


def get_latest_strikes(table_name, underlying, k_list, exps, call_list):
  """ get the latest strikes """
  query = get_query_latest('test_options', 'spy', [260], ['2018-04-09', '2018-04-18'], True)
  print query
  conn = create_mysql_session('./test-options.cnf')
  res = conn.execute(query)
  strikes = []
  for r in res:
    s = {}
    for i in range(len(COLUMN_TYPES)):
      s[COLUMN_TYPES[i]] = r[i]
    strikes.append(Strike(s))
  return strikes


def get_day_range(a, b, date_format='%Y-%m-%d'):
  """ get a range [today+a, today+b] """
  today = datetime.datetime.now().date()
  res = [today + datetime.timedelta(days=a), today + datetime.timedelta(days=b)]

  if date_format is None:
    return res
  return [datetime.datetime.strftime(x, date_format) for x in res]


def main():
  """ main function """
  strikes = get_latest_strikes('test_options', 'spy', [260], get_day_range(2,10), True)
  for s in strikes:
    print s.__json__()


if __name__ == '__main__':
  main()
