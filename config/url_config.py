from straddle.objects import objects
import os
import json

url_json_file = 'url.json'

class URLDB(objects):
  def __init__(self):
    objects.__init__(self)
    f = open(os.path.join(os.path.dirname(__file__), 'url.json'))
    g = f.read()
    f.close()
    try:
      self.data = json.loads(g)
    except:
      print 'failed to load json file: %s' % url_json_file
      self.data = None
  def getURL(self, key):
    d = self.getKey(key)
    if isinstance(d, dict):
      if 'url' in d:
        return d['url']
    return None
