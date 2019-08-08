"""It contains tests for the token management endpoint."""


from flask import json
from tests.util import create_user, get_unique_username


def test_auth_register_with_data_well_formatted_returning_200_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/register' URL is requested (POST)
    THEN check the response is valid
    """

    data = {'username': get_unique_username(), 'password': "123"}
    response = client.post('/auth/register',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['data']['username'] == data['username']


def test_auth_register_without_data_returning_400_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/register' URL is requested (POST) without data
    THEN check the response HTTP 400 response
    """
    
    response = client.post('/auth/register', content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_auth_register_without_request_content_type_returning_400_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/register' URL is requested (POST) without request content type
    THEN check the response HTTP 400 response
    """

    response = client.post('/auth/register')
    assert response.status_code == 400    
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_auth_register_with_empty_data_returning_400_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/register' URL is requested (POST) with empty data
    THEN check the response HTTP 400 response
    """

    data = {}
    response = client.post('/auth/register',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'username': 'must be filled'} in response.json['data']
    assert {'password': 'must be filled'} in response.json['data']


def test_auth_register_without_username_returning_400_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/register' URL is requested (POST) without username
    THEN check the response HTTP 400 response
    """

    data = {'password': "123"}
    response = client.post('/auth/register',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'username': 'must be filled'} in response.json['data']
    assert not {'password': 'must be filled'} in response.json['data']

 
def test_auth_register_without_password_returning_400_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/register' URL is requested (POST) without password
    THEN check the response HTTP 400 response
    """

    data = {'username': get_unique_username()}
    response = client.post('/auth/register',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert not {'username': 'must be filled'} in response.json['data']
    assert {'password': 'must be filled'} in response.json['data']


def test_auth_register_with_an_existent_username_returning_400_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/auth/register' URL is requested (POST) with an existent username
    THEN check the response HTTP 400 response
    """

    user = create_user(session)
    data = {'username': user.username, 'password': "123"}
    response = client.post('/auth/register',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'username': 'is already in use.'} in response.json['data']
