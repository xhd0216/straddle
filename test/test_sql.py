import datetime
import sqlalchemy as sa

import db.db_connect as dbc
import db.sa_api as api
import straddle.strategy as stg

engine = sa.create_engine('sqlite://')
meta = sa.MetaData(bind=engine)
test_table = sa.Table('test', meta,
  sa.Column('id', sa.Integer, primary_key=True))

meta.create_all(engine)

def test_basic_sqlalchemyl():
  ins = test_table.insert().values({'id':100})
  engine.execute(ins)

  que = test_table.select()
  res = engine.execute(que).fetchall()
  assert len(res) == 1
  assert res[0]['id'] == 100


def test_options_table():
  api.create_sql_engine()
  api.create_options_table()

  strk = stg.create_strike({'ask':1.50}, 'spy', 267, datetime.date(2018, 4, 20), True, 266.23)

  api.insert_strike(strk)
  res = api.query_options_table()

  assert len(res) == 1
  for key in dbc.COLUMN_TYPES:
    assert res[0].getKey(key) == strk.getKey(key)
