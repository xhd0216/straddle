from HTMLParser import *

class myParser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.tags = dict()

  def hasAttrs(self, attrs, key):
    for x in attrs:
      if key == x[0]:
        return True, x[1]
    return False, None

  def tagOn(self, tag):
    ## self.tags[tag] is a stack
    if tag not in self.tags:
      self.tags[tag] = 0
    self.tags[tag] += 1

  def tagOff(self, tag):
    if tag not in self.tags:
      ## encounter an end tag before a start tag, error
      ## give a warning, this is an html issue, don't handle
      self.tags[tag] = 1
    self.tags[tag] -= 1

  def isTagOn(self, tag):
    if tag not in self.tags:
      return False
    return self.tags[tag] > 0

  def handle_starttag(self, tag, attrs):
    self.tagOn(tag)

  def handle_endtag(self, tag):
    self.tagOff(tag)
