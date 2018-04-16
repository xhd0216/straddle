import argparse
import logging
import sys

from db.select import get_latest_strikes
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


def pretty_print(rows, in_the_money):
  """ pretty print """
  l = len(rows)
  template = '|'
  for i in range(l+1):
    template += "{%d:>6}|" % i
  print template.format('strike', *[x.getKey('strike') for x in rows])

  for i in range(l):
    line = [rows[i].getKey('strike')]
    for j in range(l):
      if j <= i:
        line.append('')
      else:
        # print expected return / cost
        if in_the_money:
          cost = rows[i].getKey('ask') - rows[j].getKey('bid')
        else:
          cost = -rows[i].getKey('bid') + rows[j].getKey('ask')
        if cost == 0:
          line.append('NA')
        else:
          # line.append('%.2f' % ((rows[j].getKey('strike') - rows[i].getKey('strike'))/cost))
          line.append('%.2f' % cost)
    print template.format(*line)


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
  parser.add_argument('--db-cnf',
                      help='if db config file is given, write results to db')

  opts = parser.parse_args()
  if opts.log_file:
    set_logger(level=opts.log_level, filename=opts.log_file,
               mode=opts.log_mode)
  else:
    set_logger(level=opts.log_level, out=sys.stdout)

  logging.info('retrieving options for %s', opts.symbol)

  """ get from webpage
  res = getOptionMW(opts.symbol)
  if res is None:
    # getOptionMW may return None because of page open failure
    logging.error('no data retrieved')
    return
  logging.info('%d data received', len(res))
  """

  res = get_latest_strikes(table_name='test_options',
                           underlying='spy',
                           k_list=[0, 10000],
                           exps=[opts.TTE_min, opts.TTE_max],
                           call_list=[True])

  # data preprocessing
  # step 1, filter the time range
  price = res[0].getKey('price')
  data = data_preprocessing(res,
                            [opts.TTE_min, opts.TTE_max],
                            [(1 - opts.price_range)*price,
                             (1 + opts.price_range)*price])
  # select all calls
  call_strikes = []
  for i in range(2):
    for k in sorted(data[i].keys()):
      call_strikes += data[i][k]

  # calculate implied vol
  call_vols(call_strikes, rate=0.035)

  # TODO: find all irons
  # step a: find in the money
  # step b: find out of money
  all_calls = data[1]
  for k in all_calls:
    in_money = filter(lambda x: x.getKey('strike') <= x.getKey('price'), all_calls[k])
    out_money = filter(lambda x: x.getKey('strike') > x.getKey('price'), all_calls[k])
    print "======", k, "======"
    pretty_print(in_money, True)
    pretty_print(out_money, False)


if __name__ == '__main__':
  main()
