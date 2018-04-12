import datetime
import logging
import os
from subprocess import Popen, PIPE

from straddle.strategy import create_strike


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

  dir_path = os.path.dirname(os.path.realpath(__file__))  
  p = Popen(["Rscript", os.path.join(dir_path, "greeks.R")], stdin=PIPE, stdout=PIPE, stderr=PIPE)

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
    print "========="
  output = p.communicate(input='\n')
  # output[0] = stdout, output[1] = stderr
  rc = p.returncode
  if rc != 0:
    exit(2)


def call_vols(strike_list, rate):
  """ given list of strikes, calculate the implied vols """
  dir_path = os.path.dirname(os.path.realpath(__file__))
  p = Popen(["Rscript", os.path.join(dir_path, "call_vol.R")], stdin=PIPE, stdout=PIPE, stderr=PIPE)
  para_str = ''
  for sl in strike_list:
    para_str += '%s %s %s %s %s\n' % (
               sl.getKey('price'),
               sl.getKey('strike'),
               rate, # interest rate
               sl.getTimeToExp() / 365.0,
               ## don't use 'last', it maybe out of date.
               sl.getKey('ask'))
  output = p.communicate(input=para_str)
  rc = p.returncode
  if output[1] != '':
    logging.error('error in R, return code: %s, msg: %s', rc, output[1])
    return rc
  lines = output[0].splitlines()
  assert len(lines) == len(strike_list)
  for i in range(len(lines)):
    vol = lines[i].split()[1]
    strike_list[i].addKey('impvol', float(vol))
  return 0


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
  test_implied_vol()
