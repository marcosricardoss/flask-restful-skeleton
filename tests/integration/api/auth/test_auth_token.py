"""It contains tests for /auth/token endpoint."""

from flask import json
from tests.util import create_user, create_tokens, is_token_revoked, revoke_token

def test_auth_list_tokens_of_logged_user_returning_200_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/auth/token' URL is requested (GET)
    THEN check the response is valid and for the tokens created
    """

    user = create_user(session)
    tokens = create_tokens(user.username)
    # request
    response = client.get('/auth/token',
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    # asserts
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    data = response.json['data']
    assert len(data) == 2
    assert data[0]['token_type'] == 'access'
    assert data[0]['jti'] == tokens['access']['decoded']['jti']
    assert data[1]['token_type'] == 'refresh'
    assert data[1]['jti'] == tokens['refresh']['decoded']['jti']


def test_auth_revoke_an_existent_token_returning_200_status_code(client, session, auth):
    """
    GIVEN a Flask application
    WHEN the '/auth/token/<id>' URL is requested (PUT)
    THEN check the response is valid and and for revoked token 
    """

    tokens = create_tokens('test')
    # request
    url = '/auth/token/{}'.format(tokens['refresh']['model'].id)
    data = {'revoke': True}
    response = client.put(url,
                          content_type='application/json',
                          data=json.dumps(data),
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    # asserts
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == 'Token revoked'
    assert is_token_revoked(tokens['refresh']['decoded'])


def test_auth_unrevoke_an_existent_token_returning_200_status_code(client, session, auth):
    """
    GIVEN a Flask application
    WHEN the '/auth/token/<id>' URL is requested (PUT)
    THEN check the response is valid and and for unrevoked token 
    """

    tokens = create_tokens('test')

    # revoking the refresh token
    revoke_token(tokens['refresh']['model'], 'test')

    # request for unrevoking the refresh token
    url = '/auth/token/{}'.format(tokens['refresh']['model'].id)
    data = {'revoke': False}
    response = client.put(url,
                           content_type='application/json',
                           data=json.dumps(data),
                           headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == 'Token unrevoked'    
    assert not is_token_revoked(tokens['refresh']['decoded'])


def test_auth_revoke_and_try_access_a_protected_url_returning_200_status_code(client, session, auth):
    """
    GIVEN a Flask application
    WHEN the '/auth/token' URL is requested (GET) with revoked token
    THEN check the response HTTP 401 response 
    """

    tokens = create_tokens('test')

    # revoking the refresh token
    revoke_token(tokens['access']['model'], 'test')

    # try to access a protected url
    endpoint = '/auth/token'
    response = client.get(endpoint,
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 401
    assert response.json['msg'] == 'Token has been revoked'

def test_auth_revoke_with_an_inexistent_token_id_returning_400_status_code(client, auth):
    """
    GIVEN a Flask application
    WHEN the '/auth/token/<id>' URL is requested (PUT) with an inexistent token
    THEN check the response HTTP 400 response 
    """

    response = client.put('/auth/token/9999999',
                          content_type='application/json',
                          headers=auth['access_token'])
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_auth_revoke_without_data_returning_400_status_code(client, session, auth):
    """
    GIVEN a Flask application
    WHEN the '/auth/token/<id>' URL is requested (PUT) without data
    THEN check the response HTTP 400 response 
    """

    tokens = create_tokens('test')

    # revoking the refresh token
    url = '/auth/token/{}'.format(tokens['refresh']['model'].id)
    response = client.put(url,
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_auth_revoke_without_request_content_type_returning_400_status_code(client, session, auth):
    """
    GIVEN a Flask application
    WHEN the '/auth/token/<id>' URL is requested (PUT) without request content type
    THEN check the response HTTP 400 response 
    """

    tokens = create_tokens('test')

    # revoking the refresh token
    url = '/auth/token/{}'.format(tokens['refresh']['model'].id)
    response = client.put(url,
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'   
    assert response.json['message'] == 'bad request' 


def test_auth_revoke_with_invalid_revoke_value_returning_400_status_code(client, session, auth):
    """
    GIVEN a Flask application
    WHEN the '/auth/token/<id>' URL is requested (PUT) with invalid revoke value
    THEN check the response HTTP 400 response 
    """

    tokens = create_tokens('test')

    # revoking the refresh token
    url = '/auth/token/{}'.format(tokens['refresh']['model'].id)
    data = {'revoke': "xxxxx"}
    response = client.put(url,
                          content_type='application/json',
                          data=json.dumps(data),
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'bad request'


def test_auth_revoke_that_not_existent_in_the_database_anymore_returning_404_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/auth/token/<id>' URL is requested (PUT) with a token deleted from database
    THEN check the response HTTP 404 response 
    """

    tokens = create_tokens('test')
    token_id = tokens['refresh']['model'].id

    # delete the token
    from app.model import Token
    token = session.query(Token).filter_by(id=token_id).one()
    session.delete(token)
    session.commit()

    # revoking the refresh token
    url = '/auth/token/{}'.format(token_id)
    data = {'revoke': True}
    response = client.put(url,
                          content_type='application/json',
                          data=json.dumps(data),
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 404
    assert response.json['status'] == 'fail'
    assert response.json['message'] == 'The specified token was not found'


def test_auth_token_no_existent_in_the_database_anymore_returning_400_status_code(client, session):
    """
    GIVEN a Flask application
    WHEN the '/auth/token/' URL is requested (GET) with a token deleted from database
    THEN check the response HTTP 400 response 
    """

    tokens = create_tokens('test')
    token_id = tokens['access']['model'].id

    # delete the token
    from app.model import Token
    token = session.query(Token).filter_by(id=token_id).one()
    session.delete(token)
    session.commit()

    # revoking the refresh token
    url = '/auth/token'
    response = client.get(url,
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 401
    assert response.json['msg'] == 'Token has been revoked'