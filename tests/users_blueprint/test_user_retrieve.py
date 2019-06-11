import pytest

from datetime import datetime

from flask import json
from .util import create_user, get_unique_username, get_unique_id, get_users_count


def test_user_retrieve_with_existent_user_id_returning_200_status_code(client, session, auth):
    user = create_user(session)
    endpoint = '/users/{}'.format(user.id)
    response = client.get(endpoint, headers=auth)
    assert response.status_code == 200


def test_user_retrieve_with_existent_username_returning_200_status_code(client, session, auth):
    user = create_user(session)
    endpoint = '/users/{}'.format(user.username)
    response = client.get(endpoint, headers=auth)
    assert response.status_code == 200


def test_user_retrieve_user_list_200_status_code(client, session, auth):
    user1 = create_user(session)
    user2 = create_user(session)
    users_count = get_users_count(session)

    endpoint = '/users'
    response = client.get(endpoint, headers=auth)

    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['data'][0]['username'] == user2.username
    assert response.json['data'][1]['username'] == user1.username
    assert len(response.json['data']) == users_count
    with pytest.raises(IndexError):
        assert response.json['data'][users_count]


def test_user_retrieve_with_inexistent_user_id_returning_404_status_code(client, auth):
    endpoint = '/users/{}'.format(get_unique_id)
    response = client.get(endpoint, headers=auth)
    assert response.status_code == 404


def test_user_retrieve_with_inexistent_username_returning_404_status_code(client, auth):
    endpoint = '/users/{}'.format(get_unique_username)
    response = client.get(endpoint, headers=auth)
    assert response.status_code == 404
