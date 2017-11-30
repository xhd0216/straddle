from earnings import *

json_output = '{\"data\":[{\"eps\": null, \"symbol\": \"AABA\"},{\"eps\": null, \"symbol\": \"ALCO\"},{\"eps\": 0.67, \"symbol\": \"AMBA\"},{\"eps\": -0.26, \"symbol\": \"BKS\"},{\"eps\": null, \"symbol\": \"BOSC\"},{\"eps\": null, \"symbol\": \"DCI\"},{\"eps\": 0.08, \"symbol\": \"EXPR\"},{\"eps\": 0.13, \"symbol\": \"FIVE\"},{\"eps\": null, \"symbol\": \"GENC\"},{\"eps\": null, \"symbol\": \"GLNG\"},{\"eps\": 0.46, \"symbol\": \"GMLP\"},{\"eps\": 0.4, \"symbol\": \"KR\"},{\"eps\": 0.43, \"symbol\": \"MIK\"},{\"eps\": -0.26, \"symbol\": \"NTNX\"},{\"eps\": 0.25, \"symbol\": \"PERY\"},{\"eps\": 0.34, \"symbol\": \"PFLT\"},{\"eps\": -4.46, \"symbol\": \"SHLD\"},{\"eps\": 0.08, \"symbol\": \"TITN\"},{\"eps\": -0.1, \"symbol\": \"TNP\"},{\"eps\": 1.27, \"symbol\": \"VMW\"},{\"eps\": 0.48, \"symbol\": \"ZUMZ\"}]}'
def test_yahoo_page():
  f = open('yahoo_earning_page.html')
  g = f.read()
  p = earningParser()
  p.feed(g)
  assert p.__json__() == json_output
