import urllib2
import logging

def GetURL(url, encode=False):
  try:
    f = urllib2.urlopen(url)
    g = f.read()
    f.close()
  except Exception, msg:
    logging.error('failed to open url %s, msg=%s', url, msg)
    return None
  c = f.getcode()
  if c != 200:
    logging.error('page %s not downloaded, return code: %s', url, c)
    return None
  if encode:
    if 'content-type' in f.headers:
      ct = f.headers['content-type']
      if 'charset=' in ct:
        encoding=ct.split('charset=')[-1]
        g = unicode(g, encoding)
  return g
  
