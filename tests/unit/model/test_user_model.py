"""Tests for the User model"""


from alchemy_mock.mocking import UnifiedAlchemyMagicMock
from ...util import get_unique_username

def test_create_new_user(app):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the id, username, password, serialization and string representation
    """

    username = get_unique_username()
    password = '123'

    from app.model.models import User

    session = UnifiedAlchemyMagicMock()
    user = User(username=username, password=password)
    session.add(user)
    session.commit()

    query = session.query(User).first()
    assert query.username == username
    assert query.password == password
    assert query.serialize() == {'id': str(user.id), 'username': username}
    assert str(query) == '<User %r>' % (username)