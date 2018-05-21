"""
  connection to database
"""

import datetime
import logging
import os
import sqlalchemy
from sqlalchemy import orm

from db.db_connect import TABLE_NAME, COLUMN_TYPES
from db.mysql_connect import create_mysql_session
from straddle.market_watcher_parser import getOptionMW
from straddle.strategy import Strike


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
  AND %s
  AND t.expiration >= '%s' AND t.expiration <= '%s'
  AND t.is_call IN (%s);
"""


def get_day_range(a, b, date_format='%Y-%m-%d'):
  """ get a range [today+a, today+b] """
  today = datetime.datetime.now().date()
  res = [today + datetime.timedelta(days=a), today + datetime.timedelta(days=b)]

  if date_format is None:
    return res
  return [datetime.datetime.strftime(x, date_format) for x in res]


SELECT_QUERY_TIME = """
  SELECT %s
  FROM %s t
  WHERE t.underlying = '%s'
  AND %s
  AND t.expiration >= '%s' AND t.expiration <= '%s'
  AND t.is_call IN (%s)
  AND t.query_time >= '%s' AND t.query_time < '%s';
"""

def get_query_latest(table_name='test_options',
                     underlying='spy',
                     k_list=None,
                     exps=None,
                     call_list=[True],
                     strike_in=False,
                     query_time=None):
  """ get latest strikes for given condition
      if query_time is not none, it should be a str
      like " %Y-%m-%d %H:%M:%S" (PDT).
      return the data around that time today
  """
  if not isinstance(k_list, list):
    k_list = [k_list]
  if not isinstance(exps, list):
    exps = [exps, exps]
  if isinstance(exps[0], int):
    exps = get_day_range(exps[0], exps[1])
  if not isinstance(call_list, list):
    call_list = [call_list]
  select_str = ','.join(['t.'+x for x in COLUMN_TYPES])
  if strike_in:
    strike_str = 't.strike IN (%s)' % ','.join([str(x) for x in k_list])
  else:
    strike_str = 't.strike >= %s AND t.strike <= %s' % (k_list[0], k_list[1])
  call_str = ','.join([str(x) for x in call_list])
  if query_time is None:
    query = SELECT_LATEST % (select_str, table_name, table_name, underlying, strike_str, exps[0], exps[1], call_str)
  else:
    base_time = datetime.datetime.strptime(query_time, '%Y-%m-%d %H:%M:%S')
    qt = [base_time - datetime.timedelta(minutes=15), base_time + datetime.timedelta(minutes=15)]
    qt = [datetime.datetime.strftime(x, '%Y-%m-%d %H:%M:%S') for x in qt]
    query = SELECT_QUERY_TIME % (select_str, table_name, underlying, strike_str,
                                 exps[0], exps[1], call_str, qt[0], qt[1])
  return query


def get_latest_strikes(table_name, underlying, k_list, exps, call_list, query_time):
  """ get the latest strikes """
  query = get_query_latest(table_name,
                           underlying,
                           k_list,
                           exps,
                           call_list,
                           False,
                           query_time)
  conn = create_mysql_session()
  res = conn.execute(query)
  strikes = []
  for r in res:
    s = {}
    for i in range(len(COLUMN_TYPES)):
      s[COLUMN_TYPES[i]] = r[i]
    strikes.append(Strike(s))
  return strikes


def main():
  """ main function """
  strikes = get_latest_strikes('test_options', 'spy', [260], [2,10], True)
  for s in strikes:
    print s.__json__()


if __name__ == '__main__':
  main()
