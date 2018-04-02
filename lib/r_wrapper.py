import os
from subprocess import Popen, PIPE


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

  p = Popen(["Rscript", "greeks.R"], stdin=PIPE, stdout=PIPE, stderr=PIPE)

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

greeks(None)
