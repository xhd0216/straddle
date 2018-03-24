from subprocess import Popen, PIPE

p = Popen(["Rscript", "test.R"], stdout=PIPE)

output = p.communicate()
rc = p.returncode

if rc != 0:
  exit(2)

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

lines = output[0].split('\n')
res = dict()
for line in lines:
  lin = line.split()
  if len(lin) > 1:
    res[lin[0].strip()] = float(lin[1])

def greeks(arg_dicts):
	""" wrapper to call greeks in R
			input in an array of dicts
	"""
	p = Popen(["Rscript", "test.R"], stdout=PIPE)
