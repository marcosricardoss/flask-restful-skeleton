"""This module contains abstract class used to implements the repositories."""

from __future__ import annotations
from abc import ABC, abstractmethod


class Repository(ABC):
    """The Repository abstract class declares the abstract methods to do operations in the
    database. The Repository's subclasses can provide the implementation
    of these methods.
    """

    @abstractmethod
    def get(self, model_id: int) -> object:
        """Retrieve a model register from database by its id.

        Parameters:
           model_id (int): Id of the model to be retrieved.

        Returns:
           object: a model object.
        """

        pass


    @abstractmethod
    def get_all(self) -> list:
        """Retrieves a list of all elements in the database.

        Returns:
           list: a list of model objects.
        """

        pass

    @abstractmethod
    def save(self, model: object) -> None:
        """Saves a model in the database.

        Parameters:
           model (Model): A model object.
        """

        pass

    @abstractmethod
    def update(self, model: object) -> None:
        """Update a existent model register in the database.

        Parameters:
           model (object): A model object.
        """

        pass

    @abstractmethod
    def delete(self, model: object) -> int:
        """Delete a existent model register in the database.

        Parameters:
           model (object): A model object.

        Returns:
           int: the a model id that was deleted.
        """

        pass


    @abstractmethod
    def is_invalid(self, model: object, editing: bool = False) -> list:
        """Checks if a given model object is valid.

        Parameters:
            user (User): The User model object.
            editing (bool): Indicates whether the validation is for an editing.

        Returns:
            list: A list containing the fields errors.

        """

        pass
