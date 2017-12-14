import urllib2

def GetURL(url):
  try:
    f = urllib2.urlopen(url)
    g = f.read()
    f.close()
  except:
    print 'failed to open url', url
    return None
  c = f.getcode()
  if c != 200:
    print 'return code', c
    return NonA
  if 'content-type' in f.headers:
    ct = f.headers['content-type']
    if 'charset=' in ct:
      encoding=ct.split('charset=')[-1]
      g = unicode(g, encoding)
  return g
  
