"""Tests for the TokenRepository class"""

import sqlalchemy, pytest
from datetime import datetime
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
from flask_jwt_extended import (
  create_access_token, create_refresh_token
)

def test_create_new_token_repository(app):
  """
  GIVEN the TokenRepository class
  WHEN a new TokenRepository is created
  THEN check the TokenRepository and the SQLAlchemy session instances
  """

  from app.model import TokenRepository
  token_repository = TokenRepository()

  assert isinstance(token_repository, TokenRepository)
  assert isinstance(token_repository.session, sqlalchemy.orm.scoping.scoped_session)

  
def test_the_get_user_tokens_method_of_user_repository(app):  
  """
  GIVEN the TokenRepository instance
  WHEN the get_user_tokens() method is call
  THEN check the token returned
  """

  from app.model import TokenRepository, Token
  token_repository = TokenRepository()
  token_repository.session = UnifiedAlchemyMagicMock()

  jti = "27d1b1a3-45b4-4a5f-83ed-b823f5ea1dbe"
  token_type = "access"
  user_identity = "test"
  revoked = True
  expires = datetime.now()

  token = Token(jti, token_type, user_identity, revoked, expires)  
  token_repository.session.add(token)
  token_repository.session.commit() 

  serialized_data = {
    'id': str(token.id),
    'jti': jti,
    'token_type': token_type,
    'user_identity': user_identity,
    'revoked': revoked,
    'expires': expires
  }

  result = token_repository.get_user_tokens('test')[0]
  assert result.jti == jti
  assert result.token_type == token_type
  assert result.user_identity == user_identity
  assert result.revoked == revoked
  assert result.expires == expires
  assert result.serialize() == serialized_data
  assert str(result) == '<Token %r>' % (jti)


def test_the_save_method_of_user_repository(app):   
  """
  GIVEN the TokenRepository instance
  WHEN the save() method is call
  THEN check session method calls and the token returned
  """

  from app.model import TokenRepository, Token
  token_repository = TokenRepository()
  token_repository.session = UnifiedAlchemyMagicMock()

  access_token_encoded = create_access_token("test")
  token = token_repository.save(access_token_encoded, app.config["JWT_IDENTITY_CLAIM"])

  token_repository.session.add.assert_called_once_with(token)
  token_repository.session.commit.assert_called_once_with()
  assert token.user_identity == 'test'


def test_the_change_token_revoking_method_of_user_repository(app):   
  """
  GIVEN the TokenRepository instance
  WHEN the save() method is call
  THEN check session method calls and the token revoke value
  """

  from app.model import TokenRepository, Token
  token_repository = TokenRepository()
  token_repository.session = UnifiedAlchemyMagicMock()

  token = Token()  
  token.id = 1
  token.jti = "27d1b1a3-45b4-4a5f-83ed-b823f5ea1dbe"
  token.token_type = "access"
  token.user_identity = "test"
  token.revoked = False
  token.expires = datetime.now()
  
  token_repository.session.add(token)
  token_repository.session.commit() 

  token_repository.change_token_revoking(1, "test", True)
  (token_repository
    .session.query
    .return_value
    .filter_by
    .assert_called_once_with(id=1, user_identity="test"))
  assert token.revoked == True


def test_the_change_token_revoking_method_of_user_repository_with_inexistent_token(app):   
  """
  GIVEN the TokenRepository instance
  WHEN the save() method is call with inexistent_token
  THEN check TokenNotFound exception throwing
  """

  from app.model import TokenRepository, Token
  from app.exceptions import TokenNotFound

  token_repository = TokenRepository()
  token_repository.session = UnifiedAlchemyMagicMock()

  with pytest.raises(TokenNotFound):
    token_repository.change_token_revoking(100, 'test', True) 
  

def test_the_revoke_all_tokens_method_of_user_repository(app):   
  """
  GIVEN the TokenRepository instance
  WHEN the revoke_all_tokens() method is call
  THEN check session method calls
  """

  from app.model import TokenRepository, Token
  token_repository = TokenRepository()
  token_repository.session = UnifiedAlchemyMagicMock()

  acc_token = Token()  
  acc_token.id = 1
  acc_token.jti = "27d1b1a3-45b4-4a5f-83ed-b823f5ea1dbe"
  acc_token.token_type = "access"
  acc_token.user_identity = "test"
  acc_token.revoked = False
  acc_token.expires = datetime.now()
  token_repository.session.add(acc_token)

  ref_token = Token()  
  ref_token.id = 2
  ref_token.jti = "27d1b1a3-45b4-4a5f-83ed-b823f5ea1dbd"
  ref_token.token_type = "refresh"
  ref_token.user_identity = "test"
  ref_token.revoked = False
  ref_token.expires = datetime.now()
  token_repository.session.add(ref_token)  

  token_repository.session.commit()

  token_repository.revoke_all_tokens("test")
  (token_repository
    .session
    .query
    .return_value
    .filter_by
    .assert_called_once_with(user_identity="test"))
  (token_repository.session
    .query
    .return_value
    .filter_by
    .return_value
    .update.assert_called_once_with({Token.revoked: True}))
   


def test_the_is_token_revoked_method_of_user_repository(app, mocker):  
  """
  GIVEN the TokenRepository instance
  WHEN the is_token_revoked() method is call
  THEN check session method calls
  """

  from app.model import TokenRepository, Token
  token_repository = TokenRepository()
  token_repository.session = UnifiedAlchemyMagicMock()

  token = Token()  
  token.id = 1
  token.jti = "27d1b1a3-45b4-4a5f-83ed-b823f5ea1dbe"
  token.token_type = "access"
  token.user_identity = "test"
  token.revoked = True
  token.expires = datetime.now()
  
  token_repository.session.add(token)
  token_repository.session.commit() 

  decoded_token = mocker.MagicMock()
  decoded_token['jti'] = token.jti

  result = token_repository.is_token_revoked(decoded_token)
  assert result
  (token_repository
    .session
    .query
    .return_value
    .filter_by
    .assert_called_once_with(jti=decoded_token['jti']))


def test_the_is_token_revoked_method_of_user_repository_with_inexistent_token(app, mocker): 
  """
  GIVEN the TokenRepository instance
  WHEN the is_token_revoked() method is call with inexistent token
  THEN check session method calls
  """

  from app.model import TokenRepository, Token
  token_repository = TokenRepository()
  token_repository.session = UnifiedAlchemyMagicMock()

  decoded_token = mocker.MagicMock()
  decoded_token['jti'] = "xxxxxxxxxxxxxx"

  result = token_repository.is_token_revoked(decoded_token)
  assert result
  (token_repository
    .session
    .query
    .return_value
    .filter_by
    .assert_called_once_with(jti=decoded_token['jti']))    


def test_the_is_invalid_method_of_token_repository(app):
  """
  GIVEN the TokenRepository instance
  WHEN the is_invalid() method is call
  THEN check the returned value
  """

  from app.model import TokenRepository
  token_repository = TokenRepository()

  assert token_repository.is_invalid(object) == []
