from config.url_config import *

def test_URLDB():
  urldb = URLDB()
  print urldb.getItem('testing')
  assert urldb.getItem('testing').getURL() == 'https://example.org/this_page_means_nothing.html'
