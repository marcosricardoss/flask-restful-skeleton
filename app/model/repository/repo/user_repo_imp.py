"""This module contains a concrete class of the UserRepository abstract class."""

from werkzeug.security import generate_password_hash

from app.model.models import User
from app.model.database import db_session
from app.model.repository.repo.user_repository import UserRepository

class UserRepositoryImp(UserRepository):
    """This class implements the UserRepository abstract class. 
    Contains specific method related to de User model to 
    do operation in the dabase.
    """    
    
    def get(self, user_id) -> User:
        """Retrieve a user from database by its id.

        Parameters:
           user_id (int): Id of the user model to be retrieved.

        Returns:
           object: a user model object.
        """

        pass

    def get_by_username(self, username:str) -> User:
        """Retrive a users from database by its username.

        Parameters:
           username (str): The username of the user.

        Returns:
            User: User model object.
        """

        pass
    
    def get_all(self) -> list:
        """Retrieves a list of all users from the database.

        Returns:
           list: a list of user model objects.
        """

        pass
    
    def save(self, user: User) -> None:
        """Saves a user in the database.

        Parameters:
           model (User): A user model object.
        """

        user.password = generate_password_hash(user.password)
        db_session.add(user)
        db_session.commit()
    
    def update(self, user: User) -> None:
        """Update a existent user in the database.

        Parameters:
           model (object): A user model object.
        """

        pass
    
    def delete(self, user: User) -> int:
        """Delete a existent user in the database.

        Parameters:
           model (object): A user object.

        Returns:
           int: the a user id that was deleted.
        """

        pass

    def authenticate(self, username:str, password:str) -> bool:
        """checks user authenticity by username and password.

        Parameters:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: A boolean indicating the user authenticity.
        """

        return False
        
    def is_invalid(self, user:User, editing:bool=False) -> list:
        """Checks if a given model object is valid.
        
        Parameters:
            user (User): The User model object.
            editing (bool): Indicates whether the validation is for an editing.

        Returns:
            list: A list containing the fields errors.

        """

        invalid = list()
        
        if not user.username:
            invalid.append({"username": "Must be filled"})

        """ if  not editing and self.customer_dao.get_customer_by_code(customer.code):
            invalid.append(("Código", "Já em uso para outro cliente.")) """

        if not user.password:
            invalid.append({"password": "Must be filled"})

        return invalid