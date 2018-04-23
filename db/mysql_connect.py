import logging
import os
import sqlalchemy
from sqlalchemy import orm

def get_mysql_connect(cnf):
  with open(cnf, 'r') as cobj:
    r = cobj.readlines()
  client_flag = False
  res = {}
  for line in r:
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
  if 'host' not in res:
    logging.warning('missing host in cnf file, use localhost')
    res['host'] = 'localhost'
  if 'port' not in res:
    logging.info('missing port in cnf file, use 3306')
    res['port'] = 3306
  if 'database' not in res:
    logging.warning('missing database in cnf file')
    res['database'] = ''
  if 'user' not in res:
    logging.warning('missing user in cnf file')
    return 'mysql://%(host)s:%(port)s/%(database)s' % res
  if 'password' not in res:
    logging.warning('missing password in cnf file')
    return None
  return 'mysql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s' % res


class mysqlSession():
  def __init__(self, url):
    self.engine = sqlalchemy.create_engine(url)
  def execute_multiple(self, cmds):
    """ execute multiple commands (insert update delete) in one session """
    if not cmds:
      return
    Session = orm.session.sessionmaker(bind=self.engine.engine)
    session = Session()
    try:
      for cmd in cmds:
        session.execute(sqlalchemy.text(cmd))
      session.commit()
    except Exception as msg:
      logging.error('failed to execute to database, %s', str(msg))
      session.rollback()
    finally:
      session.close()

  def execute(self, cmd):
    """ select """
    conn = self.engine.connect()
    return conn.execute(cmd).fetchall()


def create_mysql_session(cnf=None):
  if cnf is None:
    dir_name = os.path.dirname(os.path.realpath(__file__))
    cnf = os.path.join(dir_name, '../deployment/test-options.cnf')
  url = get_mysql_connect(cnf)
  if url is None:
    return None
  return mysqlSession(url)
