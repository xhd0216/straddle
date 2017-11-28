import objects

class testObjects(objects):
  def __init__(self):
    objects.__init__(self)
    self.addRequiredField('str_field', str)
    self.addRequiredField('int_field', int)
    self.addRequiredField('float_field', float)
def test_inherit_objects():
  t = testObjects()
  assert t.addKey('str_field', 1)
  assert t.addKey('int_field', '1.02')
  assert t.addKey('float_field', 3)
  assert t.isValid() 
  assert t.getKey('int_field') == 1
  assert t.getKey('float_field') == 3
  
