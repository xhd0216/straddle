import logging
import sys

def set_logger(level=logging.DEBUG, out=None, filename=None, mode='a'):
  assert level in [logging.DEBUG,
                   logging.INFO,
                   logging.WARNING,
                   logging.ERROR,
                   logging.CRITICAL]
  
  root = logging.getLogger()
  root.setLevel(level)
  
  formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s',
                                '%Y-%m-%d %H:%M:%S')

  if out in [sys.stdout, sys.stderr]:
    ## print log to stdout or stderr
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    root.addHandler(ch)
  
  if filename:
    ## print log to file
    fh = logging.FileHandler(filename=filename, mode=mode)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    root.addHandler(fh)
  
