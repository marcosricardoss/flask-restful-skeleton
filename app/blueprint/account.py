"""Blueprint to organize and group, views related
to the '/account' endpoint of HTTP REST API.
"""

from flask import (
    abort, Blueprint, request, Response, make_response, jsonify
)
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
from app.model import UserRepository, TokenRepository


bp = Blueprint('account', __name__, url_prefix='/account')


@bp.route('', methods=('GET',))
@jwt_required
def get_account():
    """Retrieves the user account.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    user_identity = get_jwt_identity()
    user = UserRepository().get_by_username(user_identity)

    if not user:
        abort(404)

    return make_response(jsonify({
        'status': 'success',
        'data': user.serialize()
    }), 200)


@bp.route('', methods=('PUT',))
@jwt_required
def update_account() -> Response:
    """Updates the user account.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    if not request.is_json:
        abort(400)

    user_identity = get_jwt_identity()
    user_repository = UserRepository()
    user = user_repository.get_by_username(user_identity)
    if not user:
        abort(404)

    # updating the user
    user.username = user_identity
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


@bp.route('', methods=('PATCH',))
@jwt_required
def patch_account() -> Response:
    """Patches the user account.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    if not request.is_json:
        abort(400)

    user_identity = get_jwt_identity()
    user_repository = UserRepository()
    user = user_repository.get_by_username(user_identity)
    if not user:
        abort(404)

    # update the object values
    for key, value in request.json.items():
        setattr(user, key, value)
    user.username = user_identity

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


@bp.route('', methods=('DELETE',))
@jwt_required
def delete_account() -> Response:
    """Deletes the user account.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    user_identity = get_jwt_identity()
    user_repository = UserRepository()
    user = user_repository.get_by_username(user_identity)

    if user:
        user_repository.delete(user)
        TokenRepository().revoke_all_tokens(user_identity)
        return make_response('', 201)

    abort(404)
