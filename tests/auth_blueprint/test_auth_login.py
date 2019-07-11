"""It contains tests for /auth/login endpoint."""


from flask import json
from flask_jwt_extended import decode_token


def test_auth_login_with_correct_credentials_passed_returning_200_status_code(client, user):
    data = {'username': 'test', 'password': 'test'}
    response = client.post('/auth/login',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 200
    assert response.json['status'] == 'success'

    access_token_decoded = decode_token(response.json['data']['access_token'])
    refresh_token_decoded = decode_token(response.json['data']['refresh_token'])

    assert access_token_decoded['identity'] == 'test'
    assert refresh_token_decoded['identity'] == 'test'
