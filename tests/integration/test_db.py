""" This module contains tests related to database operations """


import sqlalchemy


def test_sqlalchemy_base(app):
    """
    GIVEN a Flask application
    WHEN the app is initialized
    THEN check SQLAlchemy initialization 
    """

    with app.app_context():
        from app.database import Base
        assert Base.__class__ == sqlalchemy.ext.declarative.api.DeclarativeMeta


def test_session_is_open(app):
    """
    GIVEN a Flask application
    WHEN the app is initialized
    THEN check for the SQLAlchemy session 
    """

    with app.app_context():
        from app.database import db_session
        assert db_session.__class__ == sqlalchemy.orm.scoping.scoped_session


def test_session_is_close(app):
    """
    GIVEN a Flask application
    WHEN when the app context if closed
    THEN check if the session is clean
    """

    with app.app_context():
        from app.database import db_session
        from app.model.models import User

        assert db_session()._is_clean()
        db_session.add(User())
        assert not db_session()._is_clean()

    # the session returned to pool
    assert db_session()._is_clean()