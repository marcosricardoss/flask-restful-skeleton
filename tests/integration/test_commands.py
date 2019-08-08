"""Test for the line commands."""

from werkzeug.security import check_password_hash

from tests.util import get_unique_username


def test_add_user_command(runner, monkeypatch):
    """
    GIVEN a Flask application
    WHEN when the 'user' command is entered
    THEN check for the command execution
    """

    class Recorder():
        called = False

    def fake_add_user(username, password):
        Recorder.called = True

    monkeypatch.setattr('app.commands.add_user', fake_add_user)
    result = runner.invoke(args=['user', 'admin', '123'])
    assert Recorder.called

def test_function_of_add_user_command_with_data_well(session):
    """
    GIVEN the add_user function
    WHEN when the function is called
    THEN check for the user creation
    """

    from app.commands import add_user
    
    username = get_unique_username()
    password = '123'
    add_user(username, password)

    from app.model import User
    user = session.query(User).filter_by(username=username).first()
    assert user
    assert check_password_hash(user.password, password)


def test_function_of_add_user_command_with_username_already_used(session):
    """
    GIVEN the add_user function
    WHEN when the function is called with a username already in use
    THEN check for the not-creation of the user
    """

    from app.commands import add_user
    
    username = 'test'
    password = 'there-will-be-no-user-with-this-password'
    add_user(username, password)

    from app.model import User
    user = session.query(User).filter_by(username=username).first()
    assert user
    assert not check_password_hash(user.password, password)