import sqlalchemy
import testing.mysqld

def test_connect():
  with testing.mysqld.Mysqld() as mysqld:
    engine = sqlalchemy.create_engine(mysqld.url())

    res = engine.execute('show tables;').fetchall()
    assert res == []

    res = engine.execute('create table if not exists test_table (name varchar(10));')

    res = engine.execute('show tables;').fetchall()

    assert res[0][0] == 'test_table'
