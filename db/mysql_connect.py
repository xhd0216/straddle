import logging
import os
import sqlalchemy
from sqlalchemy import orm

def get_mysql_connect(cnf):
  with open(cnf, 'r') as cobj:
    r = cobj.read()
  client_flag = False
  res = {}
  for line in r.split():
    line = line.strip()
    if line == '':
      continue
    if line[0] == '#':
      # comments
      continue
    if '[client]' in line:
      client_flag = True
    elif '=' not in line:
      if client_flag:
        break
    else:
      a = line.split('=')
      res[a[0].strip()] = a[1].strip()
  if 'user' not in res:
    logging.error('missing user in cnf file')
    return None
  if 'password' not in res:
    logging.error('missing password in cnf file')
    return None
  if 'host' not in res:
    logging.warning('missing host in cnf file, use localhost')
    res['host'] = 'localhost'
  if 'port' not in res:
    logging.warning('missing port in cnf file, use 3306')
    res['port'] = 3306
  if 'database' not in res:
    logging.warnign('missing database in cnf file')
    res['database'] = ''
  return 'mysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s' % res


class mysqlSession():
  def __init__(self, url):
    self.engine = sqlalchemy.create_engine(url)
  def execute_multiple(self, cmds):
    """ execute multiple commands in one session """
    if not arr:
      return
    Session = orm.session.sessionmaker(bind=eng.engine)
    session = Session()
    try:
      for cmd in arr:
        session.execute(sqlalchemy.text(cmd))
      session.commit()
    except Exception as msg:
      logging.error('failed to execute to database, %s', str(msg))
      session.rollback()
    finally:
      session.close()

  def execute(self, cmd):
    """ select or insert """
    pass
  def fetchall(self):
    pass
  def fetchone(self):
    pass


def create_mysql_session(cnf=None):
  if cnf is None:
    cnf = os.path.join(os.path.dirname(__file__), 'test-options.cnf')
  url = get_mysql_connect(cnf)
  if url is None:
    return None
  return mysqlSession(url)
