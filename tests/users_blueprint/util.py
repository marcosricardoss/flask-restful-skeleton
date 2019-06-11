import time
from datetime import datetime
from sqlalchemy import desc
from werkzeug.security import generate_password_hash


def create_user(session):
    """Creates new user.

    Parameters:            
        session: a SLQAlchmey Session object.

    Returns:
        user: A user model object.
    """

    from app.model.models import User

    user = User()
    user.username = get_unique_username()
    user.password = generate_password_hash("123")

    session.add(user)
    session.commit()

    return user


def get_users_count(session):
    """Counts the amount of user contained in the database.

    Parameters:            
        session: a SLQAlchmey Session object.

    Returns:
        An int value corresponding to the amount of registered user.
    """

    from app.model.models import User
    return session.query(User).order_by(desc(User.id)).count()


def get_unique_username():
    """Creates a unique username string.

    Returns:
        a string containing a unique username string.
    """

    return 'user_{}'.format(get_unique_id())


def get_unique_id():
    """Creates a unique ID.

    Returns:
        a string containing a unique ID.
    """

    unique = hash(time.time())

    return unique
