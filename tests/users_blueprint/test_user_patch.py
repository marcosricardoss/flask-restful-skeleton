from datetime import datetime

from flask import json
from util import create_user, get_unique_username, get_unique_id


def test_user_patch_with_all_data_passed_returning_200_status_code(client, session, auth):
    user = create_user(session)
    endpoint = '/users/{}'.format(user.id)
    data = {'username': get_unique_username(), 'password': "x123x"}

    response = client.patch(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers=auth)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert int(response.json['data']['id']) == user.id
    assert response.json['data']['username'] == data['username']


def test_user_patch_with_inexistent_user_id_returning_404_status_code(client, auth):
    endpoint = '/users/{}'.format(get_unique_id())
    response = client.patch(endpoint, content_type='application/json', headers=auth)
    assert response.status_code == 404


def test_user_patch_without_data_returning_400_status_code(client, session, auth):
    user = create_user(session)
    endpoint = '/users/{}'.format(user.id)
    response = client.patch(endpoint, content_type='application/json', headers=auth)
    assert response.status_code == 400    


def test_user_patch_with_only_username_passed_returning_200_status_code(client, session, auth):
    user = create_user(session)
    endpoint = '/users/{}'.format(user.id)
    data = {'username': get_unique_username()}

    response = client.patch(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers=auth)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert int(response.json['data']['id']) == user.id
    assert response.json['data']['username'] == data['username']


def test_user_patch_with_only_password_passed_returning_200_status_code(client, session, auth):
    user = create_user(session)
    endpoint = '/users/{}'.format(user.id)
    data = {'password': "x123x"}

    response = client.patch(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers=auth)
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert int(response.json['data']['id']) == user.id  