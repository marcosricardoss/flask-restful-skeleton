"""This module contains the 'users' Blueprint which organize and
group, views related to the '/users' endpoint of HTTP REST API.
"""

from flask import abort, Blueprint, request, Response, make_response, jsonify

from app.model.po import User
from app.model.repository_factory import UserRepositoryFactory
from app.blueprint.authentication import auth


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('/<int:user_id>', methods=('GET',))
@auth.login_required
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
        return make_response(jsonify({
            'status': 'success',
            'data': user.serialize()
        }), 200)

    abort(404)


@bp.route('/<string:username>', methods=('GET',))
@auth.login_required
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
        return make_response(jsonify({
            'status': 'success',
            'data': user.serialize()
        }), 200)

    abort(404)


@bp.route('', methods=('GET',))
@auth.login_required
def get_users() -> Response:
    """This function is responsible to deal with GET
    requests coming from /users endpoint.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    user_repository = UserRepositoryFactory().create()
    users = user_repository.get_all()

    data = [i.serialize() for i in users]

    return make_response(jsonify({
        'status': 'success',
        'data': data
    }), 200)


@bp.route('', methods=('POST',))
@auth.login_required
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
        return make_response(jsonify({
            'status': 'success',
            'data': user.serialize()
        }), 200)
    else:
        response = make_response(jsonify({
            'status': 'fail',
            'data': is_invalid
        }), 400)

    return response


@bp.route('/<int:user_id>', methods=('PUT',))
@auth.login_required
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
        abort(404)

    # updating the user
    user.username = request.json.get('username')
    user.password = request.json.get('password')

    # validating the user
    is_invalid = user_repository.is_invalid(user)
    if not is_invalid:
        user_repository.update(user)
        response = make_response(jsonify({
            'status': 'success',
            'data': user.serialize()
        }), 200)
    else:
        response = make_response(jsonify({
            'status': 'fail',
            'data': is_invalid
        }), 400)

    return response


@bp.route('/<int:user_id>', methods=('PATCH',))
@auth.login_required
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
        abort(404)

    # update the object values
    for key, value in request.json.items():
        setattr(user, key, value)

    # validating the user
    is_invalid = user_repository.is_invalid(user)
    if not is_invalid:
        user_repository.update(user)
        response = make_response(jsonify({
            'status': 'success',
            'data': user.serialize()
        }), 200)
    else:
        response = make_response(jsonify({
            'status': 'fail',
            'data': is_invalid
        }), 400)

    return response


@bp.route('/<int:user_id>', methods=('DELETE',))
@auth.login_required
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
        return make_response('', 201)

    abort(404)