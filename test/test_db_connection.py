import sqlalchemy

from straddle.db import db_connect

def test_connect():
  engine = sqlalchemy.create_engine('sqlite://')
  db_connect.create_test_option_table(engine)
