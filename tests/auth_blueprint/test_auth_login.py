"""It contains tests for /auth/login endpoint."""

from flask import json

def test_auth_login_with_correct_credentials_passed_returning_200_status_code(client, user):
    data = {'username': 'test', 'password': 'test'}
    response = client.post('/auth/login',
                           data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 200
    assert response.json['status'] == 'success'    
