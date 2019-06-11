"""This module contains the function decorators used to control the access authorization."""


from flask_httpauth import HTTPBasicAuth
from app.model.repository.fty.user_factory import UserRepositoryFactory
from flask import make_response, jsonify
from ..output import ErrorOutput


HTTP_CODE = 401
MSG = "Could not verify your access level for that URL. You have to login with proper credentials"
HEADERS = [('WWW-Authenticate', 'Basic realm="Login Required"')]

auth = HTTPBasicAuth()
user_repository = UserRepositoryFactory().create()


@auth.verify_password
def verify_password(username, password):
    """Checks the user authenticity by username and password.

    Parameters:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        a boolean indicating the authentication.
    """

    return user_repository.authenticate(username, password)


@auth.error_handler
def unauthorized():
    """Create a response when the user has not access authorization.

    Returns:
        A flask response object.
    """

    return ErrorOutput(HTTP_CODE, MSG, HEADERS).create()
