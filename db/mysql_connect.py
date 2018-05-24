import logging
import os
import sqlalchemy
from sqlalchemy import orm

from db.sa_api import get_db_link


def get_mysql_connect(cnf):
  """ obsoleted """
  if cnf is None:
    logging.error('cnf file missing')
    return None
  return get_db_link(cnf)
  

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
