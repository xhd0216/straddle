import objects

class testObjects(objects):
  def __init__(self):
    objects.__init__(self)
    self.addRequiredField('abc', str)

def test_inherit_objects():
  t = testObjects()
  assert t.addKey('abc', 1) == False
  
