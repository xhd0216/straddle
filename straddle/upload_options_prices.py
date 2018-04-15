"""
  connection to database
"""
import argparse
import datetime
import logging
import sys

from db.db_connect import insert_multiple
from db.mysql_connect import create_mysql_session
from straddle.get_strategy import filter_date_range, filter_price_range
from straddle.market_watcher_parser import getOptionMW
from util.logger import set_logger


def filter_out_zero(rows):
  """ filter out zero ask/bid/open_int """
  res = filter(lambda x: x.getKey('ask') != 0, rows)
  res = filter(lambda x: x.getKey('bid') != 0, res)
  res = filter(lambda x: x.getKey('open_int') != 0, res)
  return res


def main():
  """ main function to insert options to db """
  parser = argparse.ArgumentParser()
  parser.add_argument('--symbol', default='spy')
  parser.add_argument('--cnf', help='config file for db')
  parser.add_argument('--log-file', help='log file')
  parser.add_argument('--log-mode', default='a',
                      help='log file mode (a or w)')
  parser.add_argument('--log-level', default='debug',help='log level')

  opts = parser.parse_args()
  if opts.log_file:
    set_logger(level=opts.log_level, filename=opts.log_file,
               mode=opts.log_mode)
  else:
    set_logger(level=opts.log_level, out=sys.stdout)
  
  logging.info("========== %s ==========", str(datetime.datetime.now()))
  session = create_mysql_session(opts.cnf)
  rows = getOptionMW(opts.symbol)
  price = rows[0].getKey('price')
  rows = filter_price_range(rows, int(price*0.85), int(price*1.15))
  rows = filter_date_range(rows, 0, 60)
  rows = filter_out_zero(rows)
  insert_multiple(session, rows)


if __name__ == '__main__':
  main()
