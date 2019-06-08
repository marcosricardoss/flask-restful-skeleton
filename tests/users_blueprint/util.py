import time
from datetime import datetime


def create_user():
    """Creates new user.

    Returns:
        user: A user model object.
    """

    from app.model.database import db_session
    from app.model.models import User

    user = User()
    user.username = get_unique_username()
    user.password = "123"

    db_session.add(user)
    db_session.commit()

    return user


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
