"""It contains tests for /auth/token endpoint."""


from flask import json
from flask_jwt_extended import decode_token

from ..util import create_user


def login_request(client, data):
    response = client.post('/auth/login',
                            data=json.dumps(data),
                            content_type='application/json')

    access_token = response.json['data']['access_token']
    refresh_token = response.json['data']['refresh_token']

    return access_token, refresh_token


def get_tokens(username):
    from app.model import TokenRepository
    tokens = TokenRepository().get_user_tokens(username)
    result = dict()
    for token in tokens:
        result[token.token_type] = token
    return result


def revoke_token(token, username):
    from app.model import TokenRepository
    TokenRepository().change_token_revoking(token.id, username, True)


def test_auth_list_tokens_of_logged_user_returning_200_status_code(client, session):
    user = create_user(session)
    data = {'username': user.username, 'password': "123"}
    access_token, refresh_token = login_request(client, data)
    access_token_decoded = decode_token(access_token)
    refresh_token_decoded = decode_token(refresh_token)
    
    # request to get token list
    response2 = client.get('/auth/token', 
                           content_type='application/json',
                           headers={'Authorization': 'Bearer ' + access_token})

    data = response2.json['data']
    assert response2.status_code == 200
    assert response2.json['status'] == 'success'
    assert len(data) == 2
    access_token_decoded['jti'] = data[0]['jti']
    refresh_token_decoded['jti'] = data[1]['jti']


def test_auth_revoke_an_existent_token_returning_200_status_code(client, session):
    user = create_user(session)
    data = {'username': user.username, 'password': "123"}       
    access_token, __ = login_request(client, data) 
    tokens_models = get_tokens(user.username)

    # revoking the refresh token
    data = {'revoke': True}
    response3 = client.put('/auth/token/'+str(tokens_models['refresh'].id),
                           content_type='application/json',
                           data=json.dumps(data),
                           headers={'Authorization': 'Bearer ' + access_token})
    assert response3.status_code == 200
    assert response3.json['status'] == 'success'
    assert response3.json['message'] == 'Token revoked'

    # checking if the refresh token is revoked
    from app.model import TokenRepository
    tokens_models = get_tokens(user.username)
    assert tokens_models['refresh'].revoked


def test_auth_unrevoke_an_existent_token_returning_200_status_code(client, session):
    user = create_user(session)
    data = {'username': user.username, 'password': "123"}       
    access_token, __ = login_request(client, data) 
    tokens_models = get_tokens(user.username)
    
    # revoking the refresh token
    revoke_token(tokens_models['refresh'], user.username)

    # unrevoking the refresh token
    data = {'revoke': False}
    response3 = client.put('/auth/token/'+str(tokens_models['refresh'].id),
                           content_type='application/json',
                           data=json.dumps(data),
                           headers={'Authorization': 'Bearer ' + access_token})
    assert response3.status_code == 200
    assert response3.json['status'] == 'success'
    assert response3.json['message'] == 'Token unrevoked'

    # checking if the refresh token is unrevoked
    from app.model import TokenRepository
    tokens_models = get_tokens(user.username)
    assert not tokens_models['refresh'].revoked


def test_auth_revoke_and_try_access_a_protected_url_returning_200_status_code(client, session):    
    user = create_user(session)
    data = {'username': user.username, 'password': "123"}       
    access_token, __ = login_request(client, data) 
    tokens_models = get_tokens(user.username)
    
    # revoking the refresh token
    revoke_token(tokens_models['access'], user.username)

    # try to access a protected url
    endpoint = '/auth/token'
    response = client.get(endpoint, headers={'Authorization': 'Bearer '+access_token})
    assert response.status_code == 401
    assert response.json['msg'] == 'Token has been revoked'


def test_auth_revoke_with_an_inexistent_token_id_returning_400_status_code(client, auth):
    response = client.put('/auth/token/9999999',
                          content_type='application/json',
                          headers=auth['access_token'])
    assert response.status_code == 400
    assert response.json['status'] == 'fail'


def test_auth_revoke_without_data_returning_400_status_code(client, session):
    user = create_user(session)
    data = {'username': user.username, 'password': "123"}       
    access_token, __ = login_request(client, data) 
    tokens_models = get_tokens(user.username)
    
    # revoking the refresh token
    response = client.put('/auth/token/'+str(tokens_models['refresh'].id),
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + access_token})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'


def test_auth_revoke_with_invalid_revoke_vaue_returning_400_status_code(client, session):
    user = create_user(session)
    data = {'username': user.username, 'password': "123"}       
    access_token, __ = login_request(client, data) 
    tokens_models = get_tokens(user.username)

    # revoking the refresh token
    data = {'revoke': "xxxxx"}
    response = client.put('/auth/token/'+str(tokens_models['refresh'].id),
                          content_type='application/json',
                          data=json.dumps(data),
                          headers={'Authorization': 'Bearer ' + access_token})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
