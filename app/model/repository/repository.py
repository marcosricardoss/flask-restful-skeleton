"""This module contains abstract class used to implements the repositories."""

from __future__ import annotations
from abc import ABC, abstractmethod

from sqlalchemy import desc

from app.model.database import db_session
from app.model.models import Model


class Repository(ABC):
    """The Repository abstract class declares the abstract methods to do operations in the
    database. The Repository's subclasses can provide the implementation
    of these methods.
    """

    def __init__(self, model_class):
        self.__model_class = model_class

    def get(self, model_id: int) -> Model:
        """Retrieve a model register from database by its id.

        Parameters:
           model_id (int): Id of the model to be retrieved.

        Returns:
           Model: a model object.
        """

        return db_session.query(self.__model_class).filter_by(id=model_id).first()

    def get_all(self) -> list:
        """Retrieves a list of all elements in the database.

        Returns:
           list: a list of model objects.
        """

        return db_session.query(self.__model_class).order_by(desc(self.__model_class.id))

    def save(self, model: Model) -> None:
        """Saves a model in the database.

        Parameters:
           model (Model): A model object.
        """

        db_session.commit()

    def update(self, model: Model) -> None:
        """Update a existent model register in the database.

        Parameters:
           model (Model): A model object.
        """

        db_session.commit()

    def delete(self, model: Model) -> int:
        """Delete a existent model register in the database.

        Parameters:
           model (Model): A model object.

        Returns:
           int: the a model id that was deleted.
        """

        deleted = db_session.delete(model)        
        db_session.commit()

        return deleted

    def delete_list(self, models):
        """Delete a list of models registered in the database.

        Parameters:
           models (list): A model object list.

        Returns:
           int: the a model id that was deleted.
        """

        deleted_list = list()
        for model in models:
            deleted = db_session.delete(model)
            deleted_list.append(deleted)

        db_session.commit()

        return deleted_list

    @abstractmethod
    def is_invalid(self, model: Model, editing: bool = False) -> list:
        """Checks if a given model object is valid.

        Parameters:
            model (Model): The model object.
            editing (bool): Indicates whether the validation is for an editing.

        Returns:
            list: A list containing the fields errors.

        """

        pass
