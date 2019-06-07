"""This module contains the 'auth' Blueprint which organize and
group, views related to the /auth endpoint of HTTP REST API.
"""

from flask import Blueprint, request, jsonify, Response

from app.model.repository.fty.user_factory import UserRepositoryFactory
from app.model.models import User


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('POST',))
def login() -> Response:
    """ """

    output = {
        "status": "success",
        "data": {}
    }

    response = jsonify(output)
    response.status_code = 200

    return response


@bp.route('/logout', methods=('POST',))
def logout() -> Response:
    """ """

    output = {
        "status": "success",
        "data": {}
    }

    response = jsonify(output)
    response.status_code = 200

    return response
