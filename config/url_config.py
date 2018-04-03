from lib.objects import objects
import os
import json

url_json_file = os.path.join(os.path.dirname(__file__), 'url.json')

class url_struct(objects):
  def __init__(self, d, name=None):
    objects.__init__(self)
    self.addField('url', str, True)
    if not isinstance(d, dict):
      print "invalid input: needs a dictionary"
      return
    if 'url' not in d:
      print "url missing"
      return
    for i in d.keys():
      if not self.addKey(i, d[i]):
        print "failed to add (%s, %s)" % (i, d[i])
    self.addKey('__name__', name)
  def getName(self):
    return self.getKey('__name__')
  def getURL(self):
    return self.getKey('url')
  def getParas(self):
    return self.getKey('paras')
  def getNumParas(self):
    a = self.getKey('paras')
    if a == None or not isinstance(a, list):
      return 0
    return len(a)

## URLDB object: holds a dict of (item, url_struct) 
class URLDB(objects):
  def __init__(self, fpath=url_json_file):
    objects.__init__(self)
    self.loadFile(fpath)
  def loadFile(self, fpath):
    try:
      f = open(fpath)
    except:
      print 'cannot find file %s' % str(fpath)
      return False
    if f == None:
      print 'failed to open file'
      return False
    g = f.read()
    f.close()
    try:
       a = json.loads(g)
    except Exception, e:
      print str(e)
      print 'failed to load json file: %s' % fpath
      return False
    for i in a:
      t = url_struct(a[i], i)
      if not t.isValid():
        print 'invalid entry: %s' % i
        continue
      self.addKey(i, t)
    return True
  def getItem(self, key):
    d = self.getKey(key)
    if isinstance(d, url_struct):
      return d
    return None
  def getURL(self, key):
    d = self.getItem(key)
    if not d:
      return None
    return d.getURL()
