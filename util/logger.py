import logging
import sys

LOG_OPTIONS = {
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

def set_logger(level='debug', out=None, filename=None, mode='a'):
  assert level in LOG_OPTIONS

  logger = logging.getLogger()
  logger.setLevel(LOG_OPTIONS[level])

  formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s',
                                '%Y-%m-%d %H:%M:%S')
  if out is None:
    logger.popagate = False
  elif out in [sys.stdout, sys.stderr]:
    ## print log to stdout or stderr
    ch = logging.StreamHandler(out)
    ch.setLevel(LOG_OPTIONS[level])
    ch.setFormatter(formatter)
    logger.addHandler(ch)

  if filename:
    ## print log to file
    fh = logging.FileHandler(filename=filename, mode=mode)
    fh.setLevel(LOG_OPTIONS[level])
    fh.setFormatter(formatter)
    logger.addHandler(fh)
