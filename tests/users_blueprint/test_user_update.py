from datetime import datetime

from flask import json
from util import create_user, get_unique_username, get_unique_id


def test_user_update_with_data_well_formatted_returning_200_status_code(client, session):
    """Test API can update a user (PUT request)"""

    user = create_user(session)
    endpoint = '/users/{}'.format(user.id)
    data = {'username': get_unique_username(), 'password': "x123x"}

    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json')
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert int(response.json['data']['id']) == user.id
    assert response.json['data']['username'] == data['username']


def test_user_update_with_inexistent_user_id_returning_404_status_code(client):
    endpoint = '/users/{}'.format(get_unique_id())
    response = client.put(endpoint, content_type='application/json')
    assert response.status_code == 404


def test_user_update_without_data_returning_400_status_code(client, session):
    user = create_user(session)
    endpoint = '/users/{}'.format(user.id)
    response = client.put(endpoint, content_type='application/json')
    assert response.status_code == 400


def test_user_update_with_empty_data_returning_400_status_code(client, session):
    user = create_user(session)
    endpoint = '/users/{}'.format(user.id)
    data = {}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'username': 'must be filled'} in response.json['data']
    assert {'password': 'must be filled'} in response.json['data']


def test_user_update_without_username_returning_400_status_code(client, session):
    user = create_user(session)
    endpoint = '/users/{}'.format(user.id)
    data = {'password': 'x123x'}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'username': 'must be filled'} in response.json['data']
    assert not {'password': 'must be filled'} in response.json['data']


def test_user_update_without_password_returning_400_status_code(client, session):
    user = create_user(session)
    endpoint = '/users/{}'.format(user.id)
    data = {'username': 'user'}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert not {'username': 'must be filled'} in response.json['data']
    assert {'password': 'must be filled'} in response.json['data']


def test_user_update_with_a_existent_username_returning_400_status_code(client, session):
    user1 = create_user(session)
    user2 = create_user(session)

    endpoint = '/users/{}'.format(user1.id)
    data = {'username': user2.username, 'password': "123"}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'username': 'is already in use.'} in response.json['data']
