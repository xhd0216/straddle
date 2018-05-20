import sqlalchemy

from db.db_connect import create_test_options_table, TABLE_NAME
from straddle.strategy import create_strike

TEST_TABLE_NAME = TABLE_NAME
def test_connect():
  engine = sqlalchemy.create_engine('sqlite://')
  create_test_options_table(engine, TEST_TABLE_NAME)
  
  conn = engine.connect()
  meta = sqlalchemy.MetaData(engine,reflect=True)
  table = meta.tables[TEST_TABLE_NAME]

  strikes_input = [
    {
      'underlying': 'SPY',
      'strike': 272,
      'expiration': '2018-05-18',
      'is_call': True,
      'price': 271.36,
    }
  ]
  
  strikes = [create_strike(x) for x in strikes_input]
  conn.execute(table.insert(), [y.data for y in strikes])
  res = conn.execute(table.select())
  for row in res:
    print row
    print row['underlying']
  assert 0

