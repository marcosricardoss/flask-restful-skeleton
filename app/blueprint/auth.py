"""Blueprint to organize and group, views related
to the '/auth' endpoint of HTTP REST API.
"""

from flask import (
    current_app, abort, Blueprint, request, Response, make_response, jsonify
)
from flask_jwt_extended import (
    jwt_required, create_access_token, create_refresh_token, get_raw_jwt,
    jwt_refresh_token_required, get_jwt_identity
)
from app.exceptions import TokenNotFound
from app.model import User, Token
from app.model import UserRepository, TokenRepository


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('POST',))
def register() -> Response:
    """Register a new user.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    if not request.is_json:
        abort(400)

    user_repository = UserRepository()

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


@bp.route('/login', methods=('POST',))
def login() -> Response:
    """Login of the user by creating a valid token.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    data = request.json

    # checkint the json data
    if not request.is_json or not data.get('username') or not data.get('password'):
        abort(400)

    # authenticating the user
    user = UserRepository().authenticate(data.get('username'), data.get('password'))
    if not user:
        response = make_response(jsonify({
            'status': 'fail',
            'message': 'Username or Password not valid'
        }), 401)

    else:
        access_token_encoded = create_access_token(identity=user.username)
        refresh_token_encoded = create_refresh_token(identity=user.username)

        token_repository = TokenRepository()
        token_repository.save(access_token_encoded,
                              current_app.config["JWT_IDENTITY_CLAIM"])
        token_repository.save(refresh_token_encoded,
                              current_app.config["JWT_IDENTITY_CLAIM"])

        response = make_response(jsonify({
            'status': 'success',
            'data': {
                'access_token': access_token_encoded,
                'refresh_token': refresh_token_encoded
            }
        }), 200)

    return response


@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """Create a new access token.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    current_user = get_jwt_identity()
    access_token_encoded = create_access_token(identity=current_user)

    token_repository = TokenRepository()
    token_repository.save(access_token_encoded,
                          current_app.config["JWT_IDENTITY_CLAIM"])

    return make_response(jsonify({
        'status': 'success',
        'data': {'access_token': access_token_encoded}
    }), 200)


@bp.route('/token', methods=('GET',))
@jwt_required
def get_tokens():
    """Retrieve all tokens of the user.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    user_identity = get_jwt_identity()
    tokens = TokenRepository().get_user_tokens(user_identity)

    data = [i.serialize() for i in tokens]

    return make_response(jsonify({
        'status': 'success',
        'data': data
    }), 200)


@bp.route('/token/<int:token_id>', methods=('PUT',))
@jwt_required
def modify_token(token_id: int):
    """Modifies the revocation status of a token.

    Parameters:
        token_id (int): Token ID to be changed.

    Returns:
        response: flask.Response object with the application/json mimetype.
    """

    if not request.is_json:
        abort(400)

    revoke = request.json.get('revoke', None)
    if revoke is None or not isinstance(revoke, bool):
        abort(400)

    # Revoke or unrevoke the token based on what was passed to this function
    user_identity = get_jwt_identity()
    try:
        token_repository = TokenRepository()
        if revoke:
            token_repository.change_token_revoking(
                token_id, user_identity, True)
            return make_response(jsonify({
                'status': 'success',
                'message': 'Token revoked'
            }), 200)
        else:
            token_repository.change_token_revoking(
                token_id, user_identity, False)
            return make_response(jsonify({
                'status': 'success',
                'message': 'Token unrevoked'
            }), 200)
    except TokenNotFound:
        return make_response(jsonify({
            'status': 'fail',
            'message': 'The specified token was not found'
        }), 404)