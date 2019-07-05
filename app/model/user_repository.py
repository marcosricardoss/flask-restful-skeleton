"""It contains UserRepository class."""

from werkzeug.security import generate_password_hash, check_password_hash

from app.database import db_session
from .models import User
from .repository import Repository


class UserRepository(Repository):
    """It Contains specific method related to de User
    model to do operation in the dabase.
    """

    def __init__(self):
        Repository.__init__(self, User)

    def get_by_username(self, username: str) -> User:
        """Retrive a users from database by its username.

        Parameters:
           username (str): The username of the user.

        Returns:
            User: User model object.
        """

        return db_session.query(User).filter_by(username=username).first()

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

        user.password = generate_password_hash(user.password)
        db_session.commit()

    def authenticate(self, username: str, password: str) -> bool:
        """checks user authenticity by username and password.

        Parameters:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            bool: A boolean indicating the user authenticity.
        """

        user = self.get_by_username(username)
        if user and check_password_hash(user.password, password):
            return True

        return False

    def is_invalid(self, user: User, editing: bool = False) -> list:
        """Checks if a given model object is valid.

        Parameters:
            user (User): The User model object.
            editing (bool): Indicates whether the validation is for an editing.

        Returns:
            list: A list containing the fields errors.

        """

        invalid = list()

        if not user.username:
            invalid.append({"username": "must be filled"})

        if not user.password:
            invalid.append({"password": "must be filled"})

        # verify if there another user with the same username
        user_checking = self.get_by_username(user.username)
        if user_checking:
            if (not user.id) or (user.id != user_checking.id):
                invalid.append({"username": "is already in use."})

        return invalid
