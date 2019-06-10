"""This module contains the 'users' Blueprint which organize and
group, views related to the '/users' endpoint of HTTP REST API.
"""

from flask import Blueprint, request, Response

from app.model.models import User
from app.model.repository.fty.user_factory import UserRepositoryFactory
from app.blueprint.authentication import requires_basic_auth
from app.blueprint.output import SuccessOutput, FailOutput, ErrorOutput, SuccessEmptyOutput


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/<int:user_id>', methods=('GET',))
def get_user(user_id: int) -> Response:
    """This function is responsible to deal with GET
    requests coming from /users/<int:id> endpoint.

    Parameters:
        id (int): The user id.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    user_repository = UserRepositoryFactory().create()
    user = user_repository.get(user_id)

    if user:
        response = SuccessOutput(status_code=200, data=user.serialize()).create()
    else:
        response = ErrorOutput(status_code=404, message="item does not exist").create()

    return response


@bp.route('/<string:username>', methods=('GET',))
def get_user_by_username(username: str) -> Response:
    """This function is responsible to deal with GET
    requests coming from /users/<string:username> endpoint.

    Parameters:
        username (str): The username of the user

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    user_repository = UserRepositoryFactory().create()
    user = user_repository.get_by_username(username)

    if user:
        response = SuccessOutput(status_code=200, data=user.serialize()).create()        
    else:
        response = ErrorOutput(status_code=404, message="item does not exist").create()

    return response


@bp.route('', methods=('GET',))
def get_users() -> Response:
    """This function is responsible to deal with GET
    requests coming from /users endpoint.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    user_repository = UserRepositoryFactory().create()
    users = user_repository.get_all()

    data = [i.serialize() for i in users]

    return SuccessOutput(status_code=200, data=data).create()


@bp.route('', methods=('POST',))
def register() -> Response:
    """This function is responsible to deal with POST
    requests coming from /users endpoint.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    user_repository = UserRepositoryFactory().create()

    # creating a User object
    user = User()
    user.username = request.json.get('username')
    user.password = request.json.get('password')

    # validating the user
    is_invalid = user_repository.is_invalid(user)
    if not is_invalid:
        user_repository.save(user)
        response = SuccessOutput(status_code=200, data=user.serialize()).create()
    else:
        response = FailOutput(status_code=400, data=is_invalid).create()

    return response


@bp.route('/<int:user_id>', methods=('PUT',))
def update(user_id: int) -> Response:
    """This function is responsible to deal with PUT
    requests coming from /users/<int:id> endpoint.

    Parameters:
        id (int): The user id.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    user_repository = UserRepositoryFactory().create()
    user = user_repository.get(user_id)

    if not user:        
        return ErrorOutput(status_code=404, message="item does not exist").create()

    # updating the user
    user.username = request.json.get('username')
    user.password = request.json.get('password')

    # validating the user
    is_invalid = user_repository.is_invalid(user)
    if not is_invalid:
        user_repository.update(user)        
        response = SuccessOutput(status_code=200, data=user.serialize()).create()        
    else:        
        response = FailOutput(status_code=400, data=is_invalid).create()

    return response


@bp.route('/<int:user_id>', methods=('PATCH',))

def patch(user_id: int) -> Response:
    """This function is responsible to deal with PUT
    requests coming from /users/<int:id> endpoint.

    Parameters:
        id (int): The user id.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    user_repository = UserRepositoryFactory().create()
    user = user_repository.get(user_id)

    if not user:
        return ErrorOutput(status_code=404, message="item does not exist").create()

    # update the object values
    for key, value in request.json.items():
        setattr(user, key, value)

    # validating the user
    is_invalid = user_repository.is_invalid(user)
    if not is_invalid:
        user_repository.update(user)        
        response = SuccessOutput(status_code=200, data=user.serialize()).create()        
    else:
        response = FailOutput(status_code=400, data=is_invalid).create()

    return response


@bp.route('/<int:user_id>', methods=('DELETE',))
def delete(user_id: int) -> Response:
    """This function is responsible to deal with DELETE
    requests coming from /users/<int:id> endpoint.

    Parameters:
        id (int): The user id.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    user_repository = UserRepositoryFactory().create()
    user = user_repository.get(user_id)
    if user:
        user_repository.delete(user)
    
    return SuccessEmptyOutput(status_code=201).create()
