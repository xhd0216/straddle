import logging

def set_logger(level, out):
  root = logging.getLogger()
  root.setLevel(level)

  ch = logging.StreamHandler(out)
  ch.setLevel(logging.DEBUG)
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  ch.setFormatter(formatter)
  root.addHandler(ch)
