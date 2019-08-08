"""It contains tests for the account updating endpoint."""

from datetime import datetime

from flask import json
from tests.util import create_user, create_tokens, get_unique_username


def test_update_account_with_data_well_formatted_returning_200_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/account' URL is requested (PUT)
    THEN check the response is valid
    """

    user = create_user(session)
    tokens = create_tokens(user.username)
    endpoint = '/account'
    data = {'password': "x123x"}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert int(response.json['data']['id']) == user.id
    assert response.json['data']['username'] == user.username


def test_update_account_with_password_length_smaller_than_3_character_returning_400_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/account' URL is requested (PUT) with invalid password value
    THEN check the response HTTP 400 response
    """

    user = create_user(session)
    tokens = create_tokens(user.username)
    endpoint = '/account'
    data = {'password': "xx"}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {"password": "minimum length of 3 characters"} in response.json['data']   


def test_update_account_with_an_user_already_excluded_returning_404_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/account' URL is requested (PUT) with inexistent user
    THEN check the response HTTP 404 response
    """

    user = create_user(session)
    tokens = create_tokens(user.username)
    # delete the user
    session.delete(user)
    session.commit()
    # request
    response = client.put('/account',
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    # asserts
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'not Found'


def test_update_account_without_data_returning_400_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/account' URL is requested (PUT) without data
    THEN check the response HTTP 400 response
    """

    user = create_user(session)
    tokens = create_tokens(user.username)
    endpoint = '/account'
    response = client.put(endpoint,
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_update_account_without_request_content_type_returning_400_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/account' URL is requested (PUT) without the request content type
    THEN check the response HTTP 400 response
    """

    user = create_user(session)
    tokens = create_tokens(user.username)
    endpoint = '/account'
    response = client.put(endpoint,
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'    


def test_update_account_with_empty_data_returning_400_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/account' URL is requested (PUT) with empty data
    THEN check the response HTTP 400 response
    """
    user = create_user(session)
    tokens = create_tokens(user.username)
    endpoint = '/account'
    data = {}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert {'password': 'must be filled'} in response.json['data']


def test_update_account_without_password_returning_400_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/account' URL is requested (PUT) without password passed
    THEN check the response HTTP 400 response
    """

    user = create_user(session)
    tokens = create_tokens(user.username)
    endpoint = '/account'
    data = {'username': 'user'}
    response = client.put(endpoint,
                          data=json.dumps(data),
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert not {'username': 'must be filled'} in response.json['data']
    assert {'password': 'must be filled'} in response.json['data']