"""It contains tests for the token management endpoint."""


from flask import json
from ..util import create_user, get_unique_username


def test_auth_register_with_data_well_formatted_returning_200_status_code(client):
    data = {'username': get_unique_username(), 'password': "123"}
    response = client.post('/auth/register',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['data']['username'] == data['username']


def test_auth_register_without_data_returning_400_status_code(client):
    response = client.post('/auth/register', content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_auth_register_without_request_content_type_returning_400_status_code(client):
    response = client.post('/auth/register')
    assert response.status_code == 400    
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_auth_register_with_empty_data_returning_400_status_code(client):
    data = {}
    response = client.post('/auth/register',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'username': 'must be filled'} in response.json['data']
    assert {'password': 'must be filled'} in response.json['data']


def test_auth_register_without_username_returning_400_status_code(client):
    data = {'password': "123"}
    response = client.post('/auth/register',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'username': 'must be filled'} in response.json['data']
    assert not {'password': 'must be filled'} in response.json['data']

 
def test_auth_register_without_password_returning_400_status_code(client):
    data = {'username': get_unique_username()}
    response = client.post('/auth/register',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert not {'username': 'must be filled'} in response.json['data']
    assert {'password': 'must be filled'} in response.json['data']


def test_auth_register_with_a_existent_username_returning_400_status_code(client, session):
    user = create_user(session)
    data = {'username': user.username, 'password': "123"}
    response = client.post('/auth/register',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'username': 'is already in use.'} in response.json['data']
