"""It contains Repository generic class."""

from abc import ABC, abstractmethod

from sqlalchemy import desc

from app.database import db_session
from .models import Model

class Repository(ABC):
    """This class implements the common methods used
    for all specific repositories classes. The subclasses
    of it can provide the implementation of these methods.
    """

    def __init__(self, model_class):
        self.__model_class = model_class
        self.session = db_session

    def get(self, model_id: int) -> Model:
        """Retrieve a model register from database by its id.

        Parameters:
           model_id (int): Id of the model to be retrieved.

        Returns:
           Model: a model object.
        """

        return self.session.query(self.__model_class).filter_by(id=model_id).first()

    def get_all(self) -> list:
        """Retrieves a list of all elements in the database.

        Returns:
           list: a list of model objects.
        """

        return self.session.query(self.__model_class).order_by(desc(self.__model_class.id))

    def save(self, model: Model) -> None:
        """Saves a model in the database.

        Parameters:
           model (Model): A model object.
        """

        self.session.add(model)
        self.session.commit()

    def update(self, model: Model) -> None:
        """Update a existent model register in the database.

        Parameters:
           model (Model): A model object.
        """

        self.session.commit()

    def delete(self, model: Model) -> int:
        """Delete a existent model register in the database.

        Parameters:
           model (Model): A model object.

        Returns:
           int: the a model id that was deleted.
        """

        deleted = self.session.delete(model)
        self.session.commit()

        return deleted

    @abstractmethod
    def is_invalid(self, model: Model) -> list:
        """Checks if a given model object is valid.

        Parameters:
            model (Model): The model object.
            editing (bool): Indicates whether the validation is for an editing.

        Returns:
            list: A list containing the fields errors.

        """

        return []
