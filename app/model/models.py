"""This module define all models (persistent objects - PO) of application. Each model
is a subclasse of the Base class (base declarative) from app.model.database module.
The declarative extension in SQLAlchemy allows to define tables and models in one go,
that is in the same class.
"""


from datetime import datetime

from sqlalchemy import inspect
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base


class Model:
    """The Model class declare the serialize() method that is
    supposed to serializes the model data. The Model's subclasses
    can provide a implementation of this method."""

    def serialize(self) -> dict:
        """Serialize the object attributes values into a dictionary."""

        return {}

    def remove_session(self):
        """Removes an object from the session its current session."""

        session = inspect(self).session
        if session:
            session.expunge(self)


class User(Base, Model):
    """ User's model class.

    Column:
        id (interger, primary key)
        username (string, unique)
        password (string)

    Attributes:
        username (str): User's username
        password (str): User's password
    """

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(), unique=True)
    password = Column(String())

    def __init__(self, username: str = None, password: str = None) -> None:
        """ The constructor for User class.

        Parameters:
            username (str): User's username
            password (str): User's password
        """

        self.username = username
        self.password = password

    def serialize(self) -> dict:
        """Serialize the object attributes values into a dictionary.

        Returns:
           dict: a dictionary containing the attributes values
        """

        data = {
            'id': str(self.id),
            'username': self.username
        }

        return data

    def __repr__(self) -> str:
        return '<User %r>' % (self.username)


class Token(Base, Model):
    """ Token's model class.

    Column:
        id (interger, primary key)
        jti (string)
        token_type (string)
        user_identity (string)
        revoked (bool)
        expires (datetime)

    Attributes:
        jti (str): Unique identifier for the JWT
        token_type (str): Token type text
        user_identity (str): User ID text
        revoked (bool): Indicates when a token has been revoked
        expires (datetime): Expiration date
    """

    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True)
    jti = Column(String(36), nullable=False)
    token_type = Column(String(10), nullable=False)
    user_identity = Column(String(50), nullable=False)
    revoked = Column(Boolean, nullable=False)
    expires = Column(DateTime, nullable=False)

    def __init__(self, jti: str = None, token_type: str = None,
                 user_identity: str = None, revoked: bool = False,
                 expires: datetime = None) -> None:
        """ The constructor for User class.

        Parameters:
            jti (str): Unique identifier for the JWT
            token_type (str): Token type text
            user_identity (str): User ID text
            revoked (bool): Indicates when a token has been revoked
            expires (datetime): Expiration date
        """

        self.jti = jti
        self.token_type = token_type
        self.user_identity = user_identity
        self.revoked = revoked
        self.expires = expires

    def serialize(self) -> dict:
        """Serialize the object attributes values into a dictionary.

        Returns:
           dict: a dictionary containing the attributes values
        """

        data = {
            'id': str(self.id),
            'jti': self.jti,
            'token_type': self.token_type,
            'user_identity': self.user_identity,
            'revoked': self.revoked,
            'expires': self.expires
        }

        return data

    def __repr__(self) -> str:
        return '<Token %r>' % (self.jti)
