import urllib2

def GetURL(url, encode=False):
  try:
    f = urllib2.urlopen(url)
    g = f.read()
    f.close()
  except Exception, msg:
    print 'failed to open url', url, msg
    return None
  c = f.getcode()
  if c != 200:
    print 'return code', c
    return None
  if encode:
    if 'content-type' in f.headers:
      ct = f.headers['content-type']
      if 'charset=' in ct:
        encoding=ct.split('charset=')[-1]
        g = unicode(g, encoding)
  return g
  
