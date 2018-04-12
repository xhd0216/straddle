import argparse
import logging
import sys

from lib.r_wrapper import call_vols
from market_watcher_parser import getOptionMW
from util.logger import set_logger


def filter_date_range(strike_array, min_days, max_days):
  """ filter the strikes that expire in date range """
  def tte_filter(x):
    """ get time to expire for strike """
    d = x.getTimeToExp()
    return d <= max_days and d >= min_days
  return filter(tte_filter, strike_array)


def filter_price_range(strike_array, min_price, max_price):
  """ filter the strikes in strike range """
  def price_filter(x):
    """ get strike in range """
    d = x.getStrike()
    return d <= max_price and d >= min_price
  return sorted(filter(price_filter, strike_array), key=lambda x: x.getStrike())

def filter_strikes_list(strike_array, price_array):
  """ price_array is a list of prices like [23, 26, 28, 31] """
  def price_filter(x):
    d = x.getStrike()
    return d in price_array # don't need to care int or float
  return filter(price_filter, strike_array)


def data_preprocessing(data_in,
                       date_range,
                       price_range):
  """ prem out unused data and sort them by date """
  tmp_list = filter_date_range(data_in, date_range[0], date_range[1])

  res = [{}, {}] # res[0] is for all put, res[1] is for all call
  for tmp in tmp_list:
    ds = tmp.getExpirationStr()
    ic = tmp.isCall()
    if ds not in res[ic]:
      res[ic][ds]= []
    res[ic][ds].append(tmp)
  for cp in range(2):
    for key in res[cp]: ## expiration dates
      res[cp][key] = filter_price_range(res[cp][key], price_range[0], price_range[1])

  return res


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--symbol', required=True)
  parser.add_argument('--TTE-min', default=1, type=int,
                      help='min time to expire')
  parser.add_argument('--TTE-max', default=10, type=int,
                      help='max time to expire')
  parser.add_argument('--price-range', default=0.1, type=float,
                      help='strike range, (1 +/- range) * current price')
  parser.add_argument('--strategy', type=str)
  parser.add_argument('--arg-list', nargs='*',
                      help='arg list for strategy')
  parser.add_argument('--log-file', help='log file')
  parser.add_argument('--log-mode', default='a',
                      help='log file mode (a or w)')
  parser.add_argument('--log-level', default='debug', help='log level')
  parser.add_argument('--db-cnf', default=False,
                      help='if db config file is given, write results to db')

  opts = parser.parse_args()
  if opts.log_file:
    set_logger(level=opts.log_level, filename=opts.log_file,
               mode=opts.log_mode)
  else:
    set_logger(level=opts.log_level, out=sys.stdout)

  logging.info('retrieving options for %s', opts.symbol)

  res = getOptionMW(opts.symbol)
  if res is None:
    # getOptionMW may return None because of page open failure
    logging.error('no data retrieved')
    return
  logging.info('%d data received', len(res))

  # data preprocessing
  # step 1, filter the time range
  price = res[0].getKey('price')
  data = data_preprocessing(res,
                            [opts.TTE_min, opts.TTE_max],
                            [(1 - opts.price_range)*price,
                             (1 + opts.price_range)*price])
  call_strikes = []
  for i in range(2):
    for k in sorted(data[1].keys()):
      print "=====", k, "====="
      for s in data[i][k]:
        print s.__json__()
        if s.isCall():
          call_strikes.append(s)
  call_vols(call_strikes, 0.035)


if __name__ == '__main__':
  main()
