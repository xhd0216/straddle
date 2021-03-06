from lib.objects import objects
import json

class testObjects(objects):
  def __init__(self):
    objects.__init__(self)
    self.addField('str_field', str, True)
    self.addField('int_field', int, True)
    self.addField('float_field', float, True)

def test_objects_to_json():
  t = testObjects()
  t.addKey('str_field', 1)
  assert not t.isValid()
  js = t.__json__()
  k = json.loads(js)
  print js
  assert len(k.keys()) == 1
  t.addKey('int_field', 1)
  t.addKey('float_field', 1.0)
  k = json.loads(t.__json__())
  assert len(k) == 3
  assert k['int_field'] == 1
  assert k['float_field'] == 1.0
  assert k['str_field'] == '1'
  assert isinstance(k['int_field'], int)
  assert isinstance(k['float_field'], float)
  # json.loads converts string to unicode
  assert isinstance(k['str_field'], unicode)
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

def test_add_required_field():
  t = testObjects()
  t.addField('str_field2', str, True)
  t.addField('str_field3', str, False)
  assert t.addKey('str_field2', 'correct key')
  assert t.getKey('str_field2')
  assert t.addKey('str_field3', 'correct key')
  assert t.getKey('str_field3')
  assert not t.getKey('str_field')
  
