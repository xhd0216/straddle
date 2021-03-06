import argparse
import logging
import sys

from db.db_connect import insert_multiple
from db.mysql_connect import create_mysql_session
from db.select import get_latest_strikes
from r.r_wrapper import call_vols
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
    return d in price_array # don't care int or float
  return filter(price_filter, strike_array)


def filter_none_zero_strike(strike_array):
  """ filter out strikes with zero ask, bid or open_int """
  def not_none(x):
    return x.getKey('ask') > 0.0 and x.getKey('bid') > 0.0 and x.getKey('open_int') > 0
  return filter(not_none, strike_array)


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
      res[cp][key] = filter_none_zero_strike(res[cp][key])
      res[cp][key] = filter_price_range(res[cp][key], price_range[0], price_range[1])

  return res


def pretty_print(rows, left):
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
        if left:
          # calculate left legs
          # cost <- influx
          cost = -rows[i].getKey('ask') + rows[j].getKey('bid')
        else:
          cost = +rows[i].getKey('bid') - rows[j].getKey('ask')
        if cost == 0:
          line.append('NA')
        else:
          line.append('%.2f' % cost)
    print template.format(*line)


AT_THE_MONEY_RATE = 0.05
def iron_table_print(data):
  # step a: find out of money puts
  # step b: find out of money calls
  for k in sorted(data[0]):
    left = filter(lambda x: x.getKey('strike') <= x.getKey('price')*(1+AT_THE_MONEY_RATE), data[0][k])
    right = filter(lambda x: x.getKey('strike') > x.getKey('price')*(1-AT_THE_MONEY_RATE), data[1][k])
    print "======", k, left[0].getKey('price'), "======"
    pretty_print(left, True)
    pretty_print(right, False)


PRINT_GREEKS = ['impvol', 'delta', 'theta', 'vega']
PRINT_BASIC = ['strike', 'ask', 'bid']

def pretty_print_strikes(rows):
  print '-' * (7* (len(rows)+1) +1)
  template = '|'
  for i in range(len(rows)+1):
    template += "{%d:>6}|" % i
  def format_helper(x, k):
    """ helper func to print format """
    r = x.getKey(k)
    if not r:
      return 'na'
    else:
      return '%.2f' % r
  for key in PRINT_BASIC + PRINT_GREEKS:
    print template.format(key, *[format_helper(x, key) for x in rows])
  print '-' * (7* (len(rows)+1) +1)


def short_bufferfly_print(data):
  """ print short butterfly """


def find_at_the_money(strikes):
  """ return the four at-the-money indexes """
  if not strikes:
    logging.debug('empty input array')
    return None
  n = len(strikes)
  price = strikes[0].getKey('price')
  if not price:
    logging.error('cannot find price')
    return None
  if n <= 4:
    return range(n)

  def helper_lambda(x):
    """ helper function to get option strike """
    return x.getKey('strike')

  index = binary_search(strikes, price, 0, n-1, helper_lambda)
  if index is None:
    logging.error('cannot find at the money strikes, price=%.2f', price)
    # it is possible: all strikes are below prices.
    return [n-2, n-1]

  if index == 0:
    logging.error('did not see strikes below price. price=%.2f, closest strike=%.2f', price, helper_lambda(strikes[index]))
    return [0, 1]
  if index == 1:
    return [0, 1, 2]

  if index == n - 1:
    logging.warning('did not see strikes above price. price=%.2f, closest strike=%.2f', price, helper_lambda(strikes[index]))
    return [index - 2, index - 1, index]

  return [index-2, index-1, index, index+1]
  
    
    
     


def pretty_print_short_condor(data, gap=0.0, spread=1.0):
  """ pretty print short condor or short butterfly """
  """
      short condor: -1 put +1 put +1 call -1 call
      gap: gap between the +put and +call
      spread: gap between the -put and +put, and between +call and -call
  """



def all_strikes_print(data):
  for k in sorted(data[0]):
    puts = data[0][k]
    calls = data[1][k]
    print "=======", calls[0].getKey('underlying'), " Calls", k, calls[0].getKey('price'), "======"
    pretty_print_strikes(calls)
    print "=======", calls[0].getKey('underlying'), "  Puts", k, calls[0].getKey('price'), "======"
    pretty_print_strikes(puts)


def strangle_table_print(data):
  # step a: find out of money puts
  # step b: find out of money calls
  for k in sorted(data[0]):
    left = filter(lambda x: x.getKey('strike') <= x.getKey('price')*(1+AT_THE_MONEY_RATE), data[0][k])
    right = filter(lambda x: x.getKey('strike') > x.getKey('price')*(1-AT_THE_MONEY_RATE), data[1][k])
    print "=======", k, left[0].getKey('price'), "======"
    pretty_print_strikes(left)
    pretty_print_strikes(right)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--from-web', action='store_true',
                      help='get data from web')
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
  parser.add_argument('--query-time', help='which time to query')

  opts = parser.parse_args()
  if opts.log_file:
    set_logger(level=opts.log_level, filename=opts.log_file,
               mode=opts.log_mode)
  else:
    set_logger(level=opts.log_level, out=sys.stdout)

  logging.info('retrieving options for %s', opts.symbol)

  if opts.from_web: 
    res = getOptionMW(opts.symbol)
    if res is None:
      # getOptionMW may return None because of page open failure
      logging.error('no data retrieved')
      return
    logging.info('%d data received', len(res))
  else:
    res = get_latest_strikes(table_name='test_options',
                             underlying=opts.symbol,
                             k_list=[0, 10000],
                             exps=[opts.TTE_min, opts.TTE_max],
                             call_list=[False, True],
                             query_time=opts.query_time)
    if not len(res):
      logging.error('no result (from db)')
      exit(0)

  # data preprocessing
  # step 1, filter the time range
  price = res[0].getKey('price')
  data = data_preprocessing(res,
                            [opts.TTE_min, opts.TTE_max],
                            [(1 - opts.price_range)*price,
                             (1 + opts.price_range)*price])

  # select all calls
  call_strikes = []
  put_strikes = []
  for k in sorted(data[1].keys()):
    call_strikes += data[1][k]
    put_strikes += data[0][k]

  # calculate implied vol
  call_vols(call_strikes, rate=0.035)
  call_vols(put_strikes, rate=0.035, isCall=False)
  for i in call_strikes + put_strikes:
    logging.debug('strike:\n%s', i.__json__())

  if opts.strategy == 'iron':
    iron_table_print(data)
  elif opts.strategy == 'strangle':
    strangle_table_print(data)
  elif opts.strategy == 'short-butterfly':
    short_bufferfly_print(data)
  else:
    all_strikes_print(data)
  
  if opts.db_cnf:
    session = create_mysql_session(opts.db_cnf)
    insert_multiple(session, call_strikes + put_strikes)
    logging.info('%s data stored to database', opts.symbol)


if __name__ == '__main__':
  main()
