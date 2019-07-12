"""It contains tests for /auth/token endpoint."""


from flask import json
from flask_jwt_extended import decode_token

from ..util import create_user


def test_auth_list_tokens_of_logged_user_returning_200_status_code(client, session):
    user = create_user(session)
    data = {'username': user.username, 'password': "123"}
    response1 = client.post('/auth/login',
                            data=json.dumps(data),
                            content_type='application/json')

    access_token = response1.json['data']['access_token']
    access_token_decoded = decode_token(response1.json['data']['access_token'])
    refresh_token_decoded = decode_token(response1.json['data']['refresh_token'])

    response2 = client.get('/auth/token', 
                           content_type='application/json',
                           headers={'Authorization': 'Bearer ' + access_token})

    data = response2.json['data']
    assert response2.status_code == 200
    assert response2.json['status'] == 'success'
    assert len(data) == 2
    access_token_decoded['jti'] = data[0]['jti']
    refresh_token_decoded['jti'] = data[1]['jti']