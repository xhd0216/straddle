import logging
import sys

class Color(Enum):
    red = 'red'
    blue = 'blue'
    green = 'green'

    def __str__(self):
        return self.value

parser = ArgumentParser()
parser.add_argument('color', type=Color, choices=list(Color))


def set_logger(level=logging.DEBUG, out=None, filename=None, mode='a'):
  assert level in [logging.DEBUG,
                   logging.INFO,
                   logging.WARNING,
                   logging.ERROR,
                   logging.CRITICAL]
  
  logger = logging.getLogger()
  logger.setLevel(level)
  
  formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s',
                                '%Y-%m-%d %H:%M:%S')
  if out is None:
    logger.popagate = False
  elif out in [sys.stdout, sys.stderr]:
    ## print log to stdout or stderr
    ch = logging.StreamHandler(out)
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
  else:
    print "here"
    logger.propagate = False
  
  if filename:
    ## print log to file
    fh = logging.FileHandler(filename=filename, mode=mode)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
