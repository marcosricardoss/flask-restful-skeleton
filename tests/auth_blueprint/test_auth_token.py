"""It contains tests for /auth/token endpoint."""

from flask import json
from ..util import create_user, create_tokens, revoke_token, is_token_revoked


def test_auth_list_tokens_of_logged_user_returning_200_status_code(client, session):
    user = create_user(session)
    tokens = create_tokens(session, user.username)
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
    tokens = create_tokens(session, 'test')
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
    tokens = create_tokens(session, 'test')

    # revoking the refresh token
    revoke_token(tokens['refresh']['model'], 'test')

    # request for unrevoking the refresh token
    url = '/auth/token/{}'.format(tokens['refresh']['model'].id)
    data = {'revoke': False}
    response3 = client.put(url,
                           content_type='application/json',
                           data=json.dumps(data),
                           headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response3.status_code == 200
    assert response3.json['status'] == 'success'
    assert response3.json['message'] == 'Token unrevoked'
    assert not is_token_revoked(tokens['refresh']['decoded'])


def test_auth_revoke_and_try_access_a_protected_url_returning_200_status_code(client, session, auth):
    tokens = create_tokens(session, 'test')

    # revoking the refresh token
    revoke_token(tokens['access']['model'], 'test')

    # try to access a protected url
    endpoint = '/auth/token'
    response = client.get(endpoint,
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 401
    assert response.json['msg'] == 'Token has been revoked'


def test_auth_revoke_with_an_inexistent_token_id_returning_400_status_code(client, auth):
    response = client.put('/auth/token/9999999',
                          content_type='application/json',
                          headers=auth['access_token'])
    assert response.status_code == 400
    assert response.json['status'] == 'fail'


def test_auth_revoke_without_data_returning_400_status_code(client, session, auth):
    tokens = create_tokens(session, 'test')

    # revoking the refresh token
    url = '/auth/token/{}'.format(tokens['refresh']['model'].id)
    response = client.put(url,
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'


def test_auth_revoke_with_invalid_revoke_value_returning_400_status_code(client, session, auth):
    user = create_user(session)
    tokens = create_tokens(session, 'test')

    # revoking the refresh token
    url = '/auth/token/{}'.format(tokens['refresh']['model'].id)
    data = {'revoke': "xxxxx"}
    response = client.put(url,
                          content_type='application/json',
                          data=json.dumps(data),
                          headers={'Authorization': 'Bearer ' + tokens['access']['enconded']})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
