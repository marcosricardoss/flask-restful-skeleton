""" This module contains tests related to database operations """


import sqlalchemy
from app.model.database import Database


def test_sqlalchemy_base(app):
    with app.app_context():
        base = Database().get_base()
        assert base.__class__ == sqlalchemy.ext.declarative.api.DeclarativeMeta


def test_session_is_open(app):
    with app.app_context():
        session = Database().get_session()
        assert session is Database().get_session()


def test_session_is_close(app):
    with app.app_context():
        session = Database().get_session()
        assert session._is_clean()
        from app.model.persistent_objects import User
        session.add(User())
        assert not session._is_clean()

    # the session returned to pool
    assert session._is_clean()


def test_init_db_command(runner, monkeypatch):
    class Recorder():
        called = False

    def fake_init_db(db_factory):
        Recorder.called = True

    monkeypatch.setattr('app.model.database.Database.create', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called
