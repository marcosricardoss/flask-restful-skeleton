"""This module define all models (persistent objects) of application. Each model
is a subclasse of the Base class (base declarative) from app.model.database module.
The declarative extension in SQLAlchemy allows to define tables and models in one go,
that is in the same class.
"""


from sqlalchemy import Column, Integer, String
from app.model.database import Base


class User(Base):
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

    def __repr__(self) -> str:
        return '<User %r>' % (self.username)
