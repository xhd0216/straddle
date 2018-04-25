import datetime
from dateutil.relativedelta import relativedelta
import logging
import math
import os
import random
from subprocess import Popen, PIPE

from straddle.strategy import create_strike

dir_path = os.path.dirname(os.path.realpath(__file__))

# the output should look like this:
"""
                bscall
Price       1.20657148
Delta       0.22138880
Gamma       0.03048601
Vega        0.28965923
Rho         0.11976830
Theta      -0.01556238
Psi        -0.12373512
Elasticity 31.19259480
"""


def par(output):
  """ parse the output of greek """
  lines = output.split('\n')
  res = dict()
  for line in lines:
    lin = line.split()
    if len(lin) > 1:
      res[lin[0].strip()] = float(lin[1])
  return res


def greeks(arg_dicts, vol=None, rate=None):
  """ wrapper to call greeks in R
      input is an array of dicts
  """
  if vol is None:
    assert 'vol' in arg_dicts[0]
  if rate is None:
    assert 'rate' in arg_dicts[0]

  p = Popen(["Rscript", os.path.join(dir_path, "greeks.R")],
            stdin=PIPE, stdout=PIPE, stderr=PIPE)

  for adi in arg_dicts:
    if vol is not None:
      adi.update({'vol':vol})
    if rate is not None:
      adi.update({'rate':rate})
    p.stdin.write('%(underlying)s %(strike)s %(vol)s %(rate)s %(tte)s\n' % adi)
    output = ''
    while True:
      line = p.stdout.readline()
      if line.strip() != '':
        output += line
      else:
        break
    print output
  output = p.communicate(input='\n')
  # output[0] = stdout, output[1] = stderr
  rc = p.returncode
  if rc != 0:
    exit(2)


def get_fair_value(s):
  """ given strike s, return the value to calculate the imp vol """
  return s.getKey('ask')


def call_vols(strike_list, rate, isCall=True, fair_value=get_fair_value):
  """ given list of strikes, calculate the implied vols """
  rscript = "call_vol.R" if isCall else "put_vol.R"
  p = Popen(["Rscript", os.path.join(dir_path, rscript)],
            stdin=PIPE, stdout=PIPE, stderr=PIPE)
  para_str = ''
  for sl in strike_list:
    para_str += '%s %s %s %s %s\n' % (
               sl.getKey('price'),
               sl.getKey('strike'),
               rate, # interest rate
               sl.getTimeToExp() / 365.0,
               ## don't use 'last', it maybe out of date.
               get_fair_value(sl))
  output = p.communicate(input=para_str)
  rc = p.returncode
  if output[1] != '':
    logging.error('error in R, return code: %s, msg: %s', rc, output[1])
  lines = output[0].splitlines()
  assert len(lines) == len(strike_list)
  for i in range(len(lines)):
    vol = lines[i].split()[1]
    try:
      vol = float(vol)
    except:
      logging.error('error in calculating imp vol: %s, strike=\n%s',
                    lines[i], strike_list[i].__json__())
      vol = 0.0
    strike_list[i].addKey('impvol', vol)
  return 0


def get_hist_quote(symbol, start='2017-01-01', force=False):
  """ get historical quotes """
  today = datetime.datetime.now().date()
  today = datetime.datetime.strftime(today, '%Y-%m-%d')
  file_path = os.path.join(dir_path, '-'.join([symbol, start, today])+'.csv')
  script_path = os.path.join(dir_path, 'hist_quote.R')
  if force or not os.path.exists(file_path):
    p = Popen(["Rscript", script_path, symbol, start, today],
              stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output = p.communicate(input='')
    rc = p.returncode
    if rc != 0:
      # if output[1] has warning but return code is 0, ignore warning
      logging.error('error in R, return code: %s, msg: %s', rc, output[1])
      return None
    if not os.path.exists(file_path):
      logging.error('error: csv file %s not found, return code %s', 
                    file_path, rc)
      return None
  ret = None
  with open(file_path, 'r') as f:
    content = f.readlines()
    ret = [x.split() for x in content]
  return ret


def binary_search(data, target, start, end, f=lambda x: x):
  """ return index i in data that is bigger than target """
  if start > end or start < 0 or end >= len(data):
    return -1
  if f(data[start]) > target:
    return start
  if f(data[end]) <= target:
    return -1
  if start == end:
    return start
  mid = (end + start) / 2
  if f(data[mid]) > target:
    if f(data[mid-1]) <= target:
      return mid
    return binary_search(data, target, start, mid-1, f)
  if f(data[mid]) == target:
    return mid + 1
  return binary_search(data, target, mid+1, end, f)


def test_binary_search():
  """ test binary_search """
  arr = sorted(random.sample(range(1, 100), 80))
  tests = random.sample(range(1, 100), 20) + [-2, -1, 0, 99, 100, 101]
  for x in tests:
    found = False
    for i in range(len(arr)):
      if arr[i] > x:
        assert i == binary_search(arr, x, 0, len(arr)-1)
        found = True
        break
    if not found:
      assert -1 == binary_search(arr, x, 0, len(arr)-1)


def calculate_vol(data):
  u = sum(data) / len(data)
  t = [(x-u)**2 for x in data]
  return math.sqrt(250 * sum(t)/(len(data)-1)) * 100


VOL_PERIODS_MONTH = [12, 9, 6, 3, 2, 1]
VOL_PERIODS_WEEK = [3, 2, 1]
def get_realized_vol(symbol):
  """ calculate realized vol """
  today = datetime.datetime.now().date()
  periods = [today - datetime.timedelta(days=m*30+1) for m in VOL_PERIODS_MONTH]
  periods += [today - datetime.timedelta(days=w*7+1) for w in VOL_PERIODS_WEEK]
  periods = [datetime.datetime.strftime(x, '%Y-%m-%d') for x in periods]
  print periods
  data = get_hist_quote(symbol, start=periods[0])[1:]
  for i in range(1, len(data)):
    data[i].append(math.log(float(data[i][2])) - math.log(float(data[i][3])))
    data[i].append(math.log(float(data[i][4])) - math.log(float(data[i-1][4])))
  for p in periods:
    # find the start date index
    index = binary_search(data, p, 0, len(data)-1, f=lambda x: x[0])
    if index == -1:
      logging.error('cannot find start date %s in data', p)
      continue
    vol1 = [x[5] for x in data[index+1:]]
    vol2 = [x[6] for x in data[index+1:]]
    print p, data[index][0]
    print calculate_vol(vol1)
    print calculate_vol(vol2)
  


def test_implied_vol():
  strike_list = []
  strike_list.append(create_strike({'ask':1.50}, 'spy', 267, datetime.datetime(2018, 4, 20), True, 266.23))
  strike_list.append(create_strike({'ask':2.50}, 'spy', 268, datetime.datetime(2018, 4, 20), True, 266.23))
  call_vols(strike_list, 0.035)
  for s in strike_list:
    print s.__json__()
  strike_list[0].getKey('impvol') == 0.1208742
  strike_list[1].getKey('impvol') == 0.2191618


if __name__ == '__main__':
  get_realized_vol('panw')
  #test_implied_vol()
  #ret = get_hist_quote(symbol='gdx', force=True)

