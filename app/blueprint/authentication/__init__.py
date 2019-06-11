"""This module contains the function decorators used to control the access authorization."""


from flask_httpauth import HTTPBasicAuth
from app.model.repository_factory import UserRepositoryFactory
from flask import make_response, jsonify


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

    msg = "Could not verify your access level for that URL. You have to login with proper credentials"

    response = make_response(jsonify({
        'status': 'error',
        'message': msg
    }), 401)
    response.headers.add('WWW-Authenticate', 'Basic realm="Login Required"')

    return response
