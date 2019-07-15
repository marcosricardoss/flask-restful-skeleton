"""Test for the line commands."""

from .util import get_unique_username
from werkzeug.security import check_password_hash

def test_add_user_command(runner, monkeypatch):
    class Recorder():
        called = False

    def fake_add_user(username, password):
        Recorder.called = True

    monkeypatch.setattr('app.commands.add_user', fake_add_user)
    result = runner.invoke(args=['user', 'admin', '123'])
    assert Recorder.called

def test_function_of_add_user_command_with_data_well(session):
    from app.commands import add_user
    
    username = get_unique_username()
    password = '123'
    add_user(username, password)

    from app.model import User
    user = session.query(User).filter_by(username=username).first()
    assert user
    assert check_password_hash(user.password, password)


def test_function_of_add_user_command_with_username_already_used(session):
    from app.commands import add_user
    
    username = 'test'
    password = 'there-will-be-no-user-with-this-password'
    add_user(username, password)

    from app.model import User
    user = session.query(User).filter_by(username=username).first()
    assert user
    assert not check_password_hash(user.password, password)