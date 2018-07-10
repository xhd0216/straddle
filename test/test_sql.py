import datetime
import os
import sqlalchemy as sa

import db.sa_api as api


def test_empty_db_engine():
  """ test create_sql_engine with db file """
  db_path = os.path.abspath('./empty.db')
  engine = api.create_sql_engine(db_path)
  table = sa.Table('test_table', sa.MetaData(),
    sa.Column('id', sa.Integer))
  query = table.select()
  res = engine.execute(query).fetchall()
  assert len(res) == 1
  assert res[0]['id'] == 10


def test_basic_sqlalchemyl():
  engine = sa.create_engine('sqlite://')
  meta = sa.MetaData(bind=engine)
  test_table = sa.Table('test', meta,
    sa.Column('id', sa.Integer, primary_key=True))

  meta.create_all(engine)

  ins = test_table.insert().values({'id':100})
  engine.execute(ins)

  que = test_table.select()
  res = engine.execute(que).fetchall()
  assert len(res) == 1
  assert res[0]['id'] == 100


def test_options_table():
  engine = api.create_sql_engine()
  api.create_options_table(engine, 'test_option_table')
  table = api.get_options_table()

  data = {
    'underlying': 'spy',
    'strike': 119.0,
    'expiration': datetime.date(2018, 8, 11),
    'price': 117,
    'bid': 3.0,
    'ask': 3.5,
    'last': 3.10,
    'open_int': 215,
    'query_time': datetime.datetime(2018, 5, 18, 10, 12, 0),
    'is_call': False
  }

  ins = table.insert().values(data)
  engine.execute(ins)

  query = table.select()
  res = engine.execute(query).fetchall()

  assert len(res) == 1
  for key in data.keys():
    assert res[0][key] == data.get(key)
