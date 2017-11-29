from objects import objects

class testObjects(objects):
  def __init__(self):
    objects.__init__(self)
    self.addRequiredField('str_field', str)
    self.addRequiredField('int_field', int)
    self.addRequiredField('float_field', float)

def test_objects_to_json():
  t = testObjects()
  t.addKey('str_field', 1)
  assert t.__json__() == ''
  t.addKey('int_field', 1)
  t.addKey('float_field', 1.0)
  assert t.__json__() == '{\"float_field\": 1.0, \"int_field\": 1, \"str_field\": \"1\"}'

def test_inherit_objects():
  t = testObjects()
  assert t.addKey('str_field', 1)
  assert t.addKey('int_field', '1.02')
  assert t.addKey('float_field', 3)
  assert t.isValid() 
  assert t.getKey('int_field') == 1
  assert t.getKey('float_field') == 3

def test_wrong_key_types():
  t = testObjects()
  assert t.addKey('str_field', 2)
  assert t.addKey('int_field', 2.5)  
  assert t.addKey('int_field', '3.06')
  assert t.isValid() == False
  assert t.addKey('float_field', '3e6')
  assert t.addKey('int_field', '4e') == False
