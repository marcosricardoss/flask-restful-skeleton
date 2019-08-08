"""It contains tests for the logining endpoint."""


from flask import json
from flask_jwt_extended import decode_token

from tests.util import get_unique_username, create_user


def test_auth_login_with_correct_credentials_passed_returning_200_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/auth/login' URL is requested (POST)
    THEN check the response is valid and the tokens creations
    """

    data = {'username': 'test', 'password': 'test'}
    response = client.post('/auth/login',
                           data=json.dumps(data),
                           content_type='application/json')

    assert response.status_code == 200
    assert response.json['status'] == 'success'

    # checks tokens created

    access_token_decoded = decode_token(response.json['data']['access_token'])
    refresh_token_decoded = decode_token(
        response.json['data']['refresh_token'])

    assert access_token_decoded['identity'] == 'test'
    assert refresh_token_decoded['identity'] == 'test'

    # checks for tokens in the database
    from app.model import Token
    assert session.query(Token).filter_by(jti=access_token_decoded['jti'],
                                          user_identity='test').first()
    assert session.query(Token).filter_by(jti=refresh_token_decoded['jti'],
                                          user_identity='test').first()


def test_auth_login_without_data_returning_400_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/login' URL is requested (POST) without data
    THEN check the response HTTP 400 response
    """

    response = client.post('/auth/login', content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_auth_login_with_empty_data_returning_400_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/login' URL is requested (POST) with empty data
    THEN check the response HTTP 400 response
    """

    response = client.post('/auth/login', data={},
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_auth_login_without_username_returning_400_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/login' URL is requested (POST) without username
    THEN check the response HTTP 400 response
    """

    data = {'password': "123"}
    response = client.post('/auth/login',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_auth_login_without_password_returning_400_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/login' URL is requested (POST) without password
    THEN check the response HTTP 400 response
    """

    data = {'username': get_unique_username()}
    response = client.post('/auth/login',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_auth_login_with_an_inexistent_username_returning_401_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/login' URL is requested (POST) with an inexistent username
    THEN check the response HTTP 401 response
    """

    data = {'username': 'xtestx', 'password': "test"}
    response = client.post('/auth/login',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 401
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'Username or Password not valid'


def test_auth_login_with_an_incorrect_password_returning_401_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/login' URL is requested (POST) with incorrect password 
    THEN check the response HTTP 401 response
    """

    data = {'username': 'test', 'password': "xtestx"}
    response = client.post('/auth/login',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 401
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'Username or Password not valid'
