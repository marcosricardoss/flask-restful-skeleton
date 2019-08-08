"""Contains useful function to the blueprint user tests."""


import time

from flask import current_app
from flask_jwt_extended import (
    decode_token, create_access_token, create_refresh_token
)
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


def create_tokens(username):
    """Create encoded token, a decode token and model token 
    for both access and refresh tokens.

    Parameters:
        session: a SLQAlchmey Session object.
        username (str): the user that owns the token.

    Returns:
        A dictionary with an encoded token, a decode token and model 
        token for both access and refresh tokens.
    """

    from app.model import Token, TokenRepository

    # access token
    access_tk_encoded = create_access_token(identity=username)
    access_tk_decoded = decode_token(access_tk_encoded)

    # refresh token
    refresh_tk_encoded = create_refresh_token(identity=username)
    refresh_tk_decoded = decode_token(refresh_tk_encoded)

    # token models
    token_repository = TokenRepository()
    access_tk_model = token_repository.save(
        access_tk_encoded, current_app.config["JWT_IDENTITY_CLAIM"])
    refresh_tk_model = token_repository.save(
        refresh_tk_encoded, current_app.config["JWT_IDENTITY_CLAIM"])

    return {
        'access': {
            'enconded': access_tk_encoded,
            'decoded': access_tk_decoded,
            'model': access_tk_model
        },
        'refresh': {
            'enconded': refresh_tk_encoded,
            'decoded': refresh_tk_decoded,
            'model': refresh_tk_model
        }
    }


def is_token_revoked(decoded_token):
    """"Checks if the given token is revoked or not.

    Parameters:
        encoded_token (str): The encoded JWT token.

    Returns:
        A boolean indicating the revoking status.
    """

    from app.model import TokenRepository
    return TokenRepository().is_token_revoked(decoded_token)


def revoke_token(token_model, username):
    """Revoking a given token.

    Parameters:
        username (str): the user that owns the token.
        token_model(Token): a token SLQAlchmey model.

    """

    from app.model import TokenRepository
    TokenRepository().change_token_revoking(token_model.id, username, True)
