"""Tests for the UserRepository class"""

import sqlalchemy
from alchemy_mock.mocking import UnifiedAlchemyMagicMock
from werkzeug.security import check_password_hash, generate_password_hash

from ...util import get_unique_username


def test_create_new_user_repository(app):
  """
  GIVEN the UserRepository class
  WHEN a new UserRepository is created
  THEN check the UserRepository and the SQLAlchemy session instances
  """

  from app.model import UserRepository
  user_repository = UserRepository()

  assert isinstance(user_repository, UserRepository)
  assert isinstance(user_repository.session,
                    sqlalchemy.orm.scoping.scoped_session)


def test_the_get_by_username_method_of_user_repository(app):
  """
  GIVEN the UserRepository class
  WHEN the method get_by_username(username) is called
  THEN check the user object returned
  """

  from app.model import UserRepository, User
  user_repository = UserRepository()
  user_repository.session = UnifiedAlchemyMagicMock()

  username = get_unique_username()
  password = '123'
  user = User(username=username, password=password)
  user_repository.session.add(user)
  user_repository.session.commit()

  result = user_repository.get_by_username(username)
  assert result.username == username
  assert result.password == password
  assert result.serialize() == {'id': str(user.id), 'username': username}
  assert str(result) == '<User %r>' % (username)


def test_the_save_method_of_user_repository(app):
  """
  GIVEN the UserRepository class
  WHEN the method get_by_username(username) is called
  THEN check session method calls and user data
  """

  from app.model import UserRepository, User
  user_repository = UserRepository()
  user_repository.session = UnifiedAlchemyMagicMock()

  username = get_unique_username()
  password = '123'
  user = User(username=username, password=password)
  user_repository.save(user)

  user_repository.session.add.assert_called_once_with(user)
  user_repository.session.commit.assert_called_once_with()

  assert user.username == username
  assert check_password_hash(user.password, password)
  assert user.serialize() == {'id': str(user.id), 'username': username}
  assert str(user) == '<User %r>' % (username)


def test_the_update_method_of_user_repository(app):
  """
  GIVEN the UserRepository class
  WHEN the method update(user) is called
  THEN check session method calls and user data
  """

  from app.model import UserRepository, User
  user_repository = UserRepository()
  user_repository.session = UnifiedAlchemyMagicMock()

  user = User(username=get_unique_username(), password="123")
  user_repository.session.add(user)
  user_repository.session.commit()

  # updating
  username_edited = get_unique_username()
  user.password = "1234"
  user.username = username_edited
  user_repository.update(user)

  # user_repository.session.commit.assert_called_once_with()
  assert check_password_hash(user.password, "1234")
  assert user.username == username_edited
  assert user.serialize() == {'id': str(user.id),
                              'username': username_edited}
  assert str(user) == '<User %r>' % (username_edited)


def test_the_authenticate_method_of_user_repository(app):
  """
  GIVEN the UserRepository class
  WHEN the method authenticate(username, password) is called
  THEN check the method returning
  """

  from app.model import UserRepository, User
  user_repository = UserRepository()
  user_repository.session = UnifiedAlchemyMagicMock()

  user = User(username=get_unique_username(),
              password=generate_password_hash("123"))
  user_repository.session.add(user)
  user_repository.session.commit()

  # correct data
  result = user_repository.authenticate(user.username, "123")
  assert result
  # wrong password
  result = user_repository.authenticate(user.username, "1234")
  assert not result
  # wrong username
  result = user_repository.authenticate("wrong_username", "123")
  assert result


def test_the_is_invalid_method_of_user_repository_with_corrent_data(app):
  """
  GIVEN the UserRepository class
  WHEN the method is_invalid(user) is called with a valid user
  THEN check return True
  """

  from app.model import UserRepository, User
  user_repository = UserRepository()
  user_repository.session = UnifiedAlchemyMagicMock()

  username = get_unique_username()
  password = '123'
  user = User(username=username, password=password)

  is_invalid = user_repository.is_invalid(user)
  assert not is_invalid


def test_the_is_invalid_method_of_user_repository_with_corrent_data_of_existent_user(app):
  """
  GIVEN the UserRepository class
  WHEN the method is_invalid(user) is called with a valid user
  THEN check return True
  """

  from app.model import UserRepository, User
  user_repository = UserRepository()
  user_repository.session = UnifiedAlchemyMagicMock()

  user = User()
  user.id = 1
  user.username = 'test'
  user.password = '123'    
  
  user_repository.session.add(user)
  user_repository.session.commit()
  
  # update
  user.username = 'test_edited'
  user.password = '1234'

  is_invalid = user_repository.is_invalid(user)
  assert not is_invalid


def test_the_is_invalid_method_of_user_repository_with_username_already_in_use(app):
  """
  GIVEN the UserRepository class
  WHEN the method is_invalid(user) is called with a invalid user
  THEN check return True
  """

  from app.model import UserRepository, User
  user_repository = UserRepository()
  user_repository.session = UnifiedAlchemyMagicMock()

  user = User()
  user.id = 1
  user.username = 'test'
  user.password = '123'    
  
  user_repository.session.add(user)
  user_repository.session.commit()
  
  user = User()
  user.username = 'test'
  
  is_invalid = user_repository.is_invalid(user)
  assert is_invalid
  assert {"username": "is already in use."} in is_invalid


def test_the_is_invalid_method_of_user_repository_missing_password(app):
  """
  GIVEN the UserRepository class
  WHEN the method is_invalid(user) is called with a invalid user
  THEN check return false
  """

  from app.model import UserRepository, User
  user_repository = UserRepository()
  user_repository.session = UnifiedAlchemyMagicMock()

  user = User(username="test")
  is_invalid = user_repository.is_invalid(user)

  assert is_invalid
  assert {"password": "must be filled"} in is_invalid


def test_the_is_invalid_method_of_user_repository_missing_username(app):
  """
  GIVEN the UserRepository class
  WHEN the method is_invalid(user) is called with a invalid user
  THEN check return false
  """

  from app.model import UserRepository, User
  user_repository = UserRepository()
  user_repository.session = UnifiedAlchemyMagicMock()

  user = User(password="123")
  is_invalid = user_repository.is_invalid(user)

  assert is_invalid
  assert {"username": "must be filled"} in is_invalid   


def test_the_is_invalid_method_of_user_repository_with_invalid_password(app):
  """
  GIVEN the UserRepository class
  WHEN the method is_invalid(user) is called with a invalid user
  THEN check return false
  """

  from app.model import UserRepository, User
  user_repository = UserRepository()
  user_repository.session = UnifiedAlchemyMagicMock()

  user = User(password="12")
  is_invalid = user_repository.is_invalid(user)

  assert is_invalid
  assert {"password": "minimum length of 3 characters"} in is_invalid 
