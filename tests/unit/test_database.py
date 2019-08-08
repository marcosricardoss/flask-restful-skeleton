"""It contains tests for the database.py module"""

import sqlalchemy

def test_database_init(app):
  """
  GIVEN the init() function
  WHEN init() is call
  THEN check sqlalchemy initialization
  """

  from app.database import init, Base, engine, db_session

  init(app)

  assert Base.__class__ == sqlalchemy.ext.declarative.api.DeclarativeMeta
  assert engine.__class__ == sqlalchemy.engine.base.Engine
  assert db_session.__class__ == sqlalchemy.orm.scoping.scoped_session

def test_session_shutdown(app, mocker):
  """
  GIVEN the shutdown_session() function
  WHEN shutdown_session() is call
  THEN check if the session is clean
  """

  from app.database import init, shutdown_session, db_session
  from app.database import shutdown_session

  init(app)
  db_session = mocker.MagicMock()  
  shutdown_session()

  assert db_session()._is_clean()