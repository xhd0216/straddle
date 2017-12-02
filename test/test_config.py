from config import URLDB

def test_URLDB():
  urldb = URLDB()
  assert urldb.getItem('testing') == 'https://example.org/this_page_means_nothing.html'
