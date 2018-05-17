import random

from util.misc import binary_search

def test_binary_search():
  """ test binary_search """
  arr = sorted(random.sample(range(1, 100), 80))
  tests = random.sample(range(1, 100), 20) + [-2, -1, 0, 99, 100, 101]
  for x in tests:
    found = False
    for i in range(len(arr)):
      if arr[i] > x:
        assert i == binary_search(arr, x, 0, len(arr)-1)
        found = True
        break
    if not found:
      assert binary_search(arr, x, 0, len(arr)-1) is None
