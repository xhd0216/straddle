py_test(
  name="test_mw",
  srcs = [
    "testing.py",
    "test_mw.py", 
  ],
  main="testing.py",
  deps = [
    "//straddle:market_watcher_parser"
  ],
  data = [
    "market_watch_empty.html"
  ],
  timeout="short"
)
py_test(
  name="test_insider",
  srcs = [
    "test_insider.py", 
  ],
  main="test_insider.py",
  deps = [
    "//straddle:insider_parser",
    "//util:misc",
  ],
  data = [
    "insider.html"
  ],
  timeout="short"
)

