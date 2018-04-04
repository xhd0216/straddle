"""
  connection to database
"""

import datetime
import logging
import sqlalchemy
from sqlalchemy import orm

from mysql_connect import get_mysql_connect
from straddle.market_watcher_parser import getOptionMW
from straddle.strategy import Strike


SELECT_ALL = """
  select * from %s where %s;
"""

