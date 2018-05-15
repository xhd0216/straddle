import sqlalchemy

from sqlalchemy import Table, Column, Integer, Float, String, Date, DateTime, MetaData


def create_test_options_table(engine, test_table_name='test_options'):
  metadata = MetaData()
  share_table = Table(test_table_name, metadata,
                      Column('recordid', Integer, primary_key=True),
                      Column('vfundid', Integer, nullable=False),
                      Column('class', String(length=15), nullable=False),
                      Column('fraction', Float, nullable=False),
                      Column('start_date', Date, nullable=False),
                      Column('end_date', Date, nullable=False),
                      Column('created_utc', DateTime, nullable=False),
                      Column('updated_utc', DateTime, nullable=False))
  metadata.create_all(engine)

def test_connect():
  engine = sqlalchemy.create_engine('sqlite://')

  res = engine.execute('show tables;').fetchall()
  assert res == []

  res = engine.execute('create table if not exists test_table (name varchar(10));')

  res = engine.execute('show tables;').fetchall()

  assert res[0][0] == 'test_table'
