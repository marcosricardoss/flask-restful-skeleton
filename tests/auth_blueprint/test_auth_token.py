"""It contains tests for /auth/token endpoint."""


from flask import json
from flask_jwt_extended import decode_token

from ..util import create_user


def test_auth_list_tokens_of_logged_user_returning_200_status_code(client, session):
    user = create_user(session)
    data = {'username': user.username, 'password': "123"}
    
    # login request
    response1 = client.post('/auth/login',
                            data=json.dumps(data),
                            content_type='application/json')

    access_token = response1.json['data']['access_token']
    access_token_decoded = decode_token(response1.json['data']['access_token'])
    refresh_token_decoded = decode_token(response1.json['data']['refresh_token'])
    
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
    
    # login request
    response1 = client.post('/auth/login',
                           data=json.dumps(data),
                           content_type='application/json')
    access_token = response1.json['data']['access_token']
   
    # getting the user tokens
    from app.model import TokenRepository
    tokens = TokenRepository().get_user_tokens(user.username)

    # revoking the refresh token
    data = {'revoke': True}
    response3 = client.put('/auth/token/'+str(tokens[1].id),
                           content_type='application/json',
                           data=json.dumps(data),
                           headers={'Authorization': 'Bearer ' + access_token})
    assert response3.status_code == 200
    assert response3.json['status'] == 'success'
    assert response3.json['message'] == 'Token revoked'

    # checking if the refresh token is revoked
    from app.model import TokenRepository
    tokens = TokenRepository().get_user_tokens(user.username)
    assert tokens[1].revoked


def test_auth_unrevoke_an_existent_token_returning_200_status_code(client, session):
    user = create_user(session)
    data = {'username': user.username, 'password': "123"}
    
    # login request
    response1 = client.post('/auth/login',
                            data=json.dumps(data),
                            content_type='application/json')
    access_token = response1.json['data']['access_token']

    # getting the user tokens
    from app.model import TokenRepository
    token_repository = TokenRepository()
    tokens = token_repository.get_user_tokens(user.username)
    
    # revoking the refresh token
    token_repository.change_token_revoking(tokens[1].id, user.username, True)

    # unrevoking the refresh token
    data = {'revoke': False}
    response3 = client.put('/auth/token/'+str(tokens[1].id),
                           content_type='application/json',
                           data=json.dumps(data),
                           headers={'Authorization': 'Bearer ' + access_token})
    assert response3.status_code == 200
    assert response3.json['status'] == 'success'
    assert response3.json['message'] == 'Token unrevoked'

    # checking if the refresh token is unrevoked
    from app.model import TokenRepository
    tokens = TokenRepository().get_user_tokens(user.username)
    assert not tokens[1].revoked
    

def test_auth_revoke_with_an_inexistent_token_id_returning_400_status_code(client, auth):
    response = client.put('/auth/token/9999999',
                          content_type='application/json',
                          headers=auth['access_token'])
    assert response.status_code == 400
    assert response.json['status'] == 'fail'


def test_auth_revoke_without_data_returning_400_status_code(client, session):
    user = create_user(session)
    data = {'username': user.username, 'password': "123"}
    
    # login request
    response1 = client.post('/auth/login',
                            data=json.dumps(data),
                            content_type='application/json')
    access_token = response1.json['data']['access_token']
    
    # getting the user tokens
    from app.model import TokenRepository
    tokens = TokenRepository().get_user_tokens(user.username)
    
    # revoking the refresh token
    response = client.put('/auth/token/'+str(tokens[1].id),
                          content_type='application/json',
                          headers={'Authorization': 'Bearer ' + access_token})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'


def test_auth_revoke_with_invalid_revoke_vaue_returning_400_status_code(client, session):
    user = create_user(session)
    data = {'username': user.username, 'password': "123"}
    
    # login request
    response1 = client.post('/auth/login',
                            data=json.dumps(data),
                            content_type='application/json')
    access_token = response1.json['data']['access_token']
    
    # getting the user tokens
    from app.model import TokenRepository
    tokens = TokenRepository().get_user_tokens(user.username)
    
    # revoking the refresh token
    data = {'revoke': "xxxxx"}
    response = client.put('/auth/token/'+str(tokens[1].id),
                          content_type='application/json',
                          data=json.dumps(data),
                          headers={'Authorization': 'Bearer ' + access_token})
    assert response.status_code == 400
    assert response.json['status'] == 'fail'
