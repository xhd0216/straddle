import os
from subprocess import Popen, PIPE
import tempfile


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


def greeks(arg_dicts):
	""" wrapper to call greeks in R
			input in an array of dicts
	"""
	new_file, filename = tempfile.mkstemp()
	print filename
	os.write(new_file, "this is some content")
	os.close(new_file)
	p = Popen(["Rscript", "greeks.R"], stdin=PIPE, stdout=PIPE, stderr=PIPE)

	output = p.communicate(input=filename + '\n' + 'abc' + '\n')
	# output[0] = stdout, output[1] = stderr
	rc = p.returncode
	if rc != 0:
	  exit(2)
	print par(output[0])
	print output[1]


greeks(None)
