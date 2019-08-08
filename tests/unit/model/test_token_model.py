"""Tests for the Token model"""

from datetime import datetime
from alchemy_mock.mocking import UnifiedAlchemyMagicMock

def test_create_new_token(app):
    """
    GIVEN a Token model
    WHEN a new token is created
    THEN check the id, jti, token_type, user_identity, revoked,
    expires serialization and string representation
    """

    from app.model.models import Token

    jti = "27d1b1a3-45b4-4a5f-83ed-b823f5ea1dbe"
    token_type = "access"
    user_identity = "test"
    revoked = True
    expires = datetime.now()

    session = UnifiedAlchemyMagicMock()
    token = Token(jti, token_type, user_identity, revoked, expires)
    session.add(token)
    session.commit()

    serialized_data = {
        'id': str(token.id),
        'jti': jti,
        'token_type': token_type,
        'user_identity': user_identity,
        'revoked': revoked,
        'expires': expires
    }

    query = session.query(Token).first()
    assert query.jti == jti
    assert query.token_type == token_type
    assert query.user_identity == user_identity
    assert query.revoked == revoked
    assert query.expires == expires
    assert query.serialize() == serialized_data
    assert str(query) == '<Token %r>' % (jti)
  