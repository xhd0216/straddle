import sqlalchemy

from straddle.db import db_connect

TEST_TABLE_NAME = db_connect.TABLE_NAME
def test_connect():
  engine = sqlalchemy.create_engine('sqlite://')
  db_connect.create_test_option_table(engine, TEST_TABLE_NAME)
  
  conn = engine.connect()
  meta = MetaData(engine,reflect=True)
  table = meta.tables[TEST_TABLE_NAME]

  conn.execute(table.insert(),[
     {'l_name':'Hi','f_name':'bob'},
     {'l_name':'yo','f_name':'alice'}])
