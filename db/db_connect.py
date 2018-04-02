import logging
import sqlalchemy

from mysql_connect import get_mysql_connect

def get_engine(cnf):
  return sqlalchemy.create_engine(get_mysql_connect(cnf))

if __name__ == '__main__':
  eng = get_engine('/home/joe/codes/config-straddle/test-mysql.cnf')
  res = eng.execute('show tables;').fetchall()
  print res
