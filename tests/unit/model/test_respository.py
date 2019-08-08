"""Tests for the Repository class"""

import pytest
from sqlalchemy import desc, Column, Integer
from alchemy_mock.mocking import AlchemyMagicMock

def test_create_new_repository(app):
  """
  GIVEN the Repository abstract class
  THEN the abstract methods
  """  
  from app.model.repository import Repository
  assert Repository.__dict__["__abstractmethods__"] == {'is_invalid'}  

  """
  GIVEN the Repository abstract class
  WHEN a new Repository is created
  THEN check a TypeError except
  """
  
  with pytest.raises(TypeError):
        Repository(object) 


def test_the_get_method_of_the_repository(app):  
  """
  GIVEN the Repository class
  WHEN the method get(object) is called
  THEN check session method calls
  """

  from app.model.repository import Repository
  Repository.__abstractmethods__ = frozenset()
 
  repository = Repository(object)
  repository.session = AlchemyMagicMock()
  repository.get(object)

  repository.session.query.return_value.filter_by.assert_called_once_with(id=object)


def test_the_get_all_method_of_the_repository(app, mocker):  
  """
  GIVEN the Repository class
  WHEN the method get_all(object) is called
  THEN check session method calls
  """

  from app.model.repository import Repository
  Repository.__abstractmethods__ = frozenset()
 
  # mocking the model class
  mock = mocker.MagicMock()
  mock.id = Column(Integer, primary_key=True)

  repository = Repository(mock)
  repository.session = AlchemyMagicMock()
  repository.get_all()

  repository.session.query.return_value.order_by.assert_called_once_with(desc(mock.id))  


def test_the_save_method_of_the_repository(app):  
  """
  GIVEN the Repository class
  WHEN the method save(object) is called
  THEN check session method calls
  """

  from app.model.repository import Repository
  Repository.__abstractmethods__ = frozenset()
 
  repository = Repository(object)
  repository.session = AlchemyMagicMock()
  repository.save(object)

  repository.session.add.assert_called_once_with(object)
  repository.session.commit.assert_called_once_with()
  

def test_the_update_method_of_the_repository():  
  """
  GIVEN the Repository class
  WHEN the method update(object) is called
  THEN check session method calls
  """

  from app.model.repository import Repository
  Repository.__abstractmethods__ = frozenset()
 
  repository = Repository(object)
  repository.session = AlchemyMagicMock()
  repository.update(object)
  
  repository.session.commit.assert_called_once_with()  


def test_the_delete_method_of_the_repository():  
  """
  GIVEN the Repository class
  WHEN the method delete(object) is called
  THEN check session method calls
  """

  from app.model.repository import Repository
  Repository.__abstractmethods__ = frozenset()
 
  repository = Repository(object)
  repository.session = AlchemyMagicMock()
  repository.delete(object)
  
  repository.session.delete.assert_called_once_with(object)
  repository.session.commit.assert_called_once_with()   


def test_the_is_invalid_method_of_the_repository():  
  """
  GIVEN the Repository class
  WHEN the method is_invalid(object) is called
  THEN check the method return
  """

  from app.model.repository import Repository
  Repository.__abstractmethods__ = frozenset()
 
  repository = Repository(object)
  assert repository.is_invalid(object) == []