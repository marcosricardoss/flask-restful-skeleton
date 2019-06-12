"""This module contains the abstract class used to implements user repositories."""


from abc import abstractmethod

from app.model.repository.repository import Repository
from app.model.po import User


class UserRepository(Repository):
    """UserRepository is subclass of the Repository abstract class that
    provides specific abstract methods related to the User model.
    """

    @abstractmethod
    def get_by_username(self, username: str) -> User:
        """Retrive a user by username.

        Parameters:
           username (str): The username of the user.

        Returns:
            User: User model object.
        """

        pass

    @abstractmethod
    def authenticate(self, username: str, password: str) -> bool:
        """checks user authenticity by username and password.

        Parameters:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: A boolean indicating the user authenticity.
        """

        pass
