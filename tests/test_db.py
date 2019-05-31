import pytest
import sqlalchemy
from app.model.database import DBFactory


def test_sqlalchemy_base(app):    
    with app.app_context():        
        base = DBFactory().get_base()
        assert base.__class__ == sqlalchemy.ext.declarative.api.DeclarativeMeta


def test_session_is_open(app):    
    with app.app_context():                
        session = DBFactory().get_session()
        assert session.__class__ == sqlalchemy.orm.scoping.scoped_session
        assert session is DBFactory().get_session()        


def test_session_is_close(app):    
    with app.app_context():        
        session = DBFactory().get_session()        
    
    with pytest.raises(Exception) as e:
        assert DBFactory().get_session()        

    assert e


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db(db_factory):        
        Recorder.called = True

    monkeypatch.setattr('app.model.database.DBFactory.create', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called