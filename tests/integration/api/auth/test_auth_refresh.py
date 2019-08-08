"""It contains tests for the token refresh endpoint."""

from flask_jwt_extended import decode_token


def test_auth_refresh_a_valid_token_returning_200_status_code(client, session, auth):
    """
    GIVEN a Flask application
    WHEN the '/auth/login' URL is requested (POST)
    THEN check the response is valid and for the created tokens
    """
    
    response = client.post('/auth/refresh',
                           content_type='application/json',
                           headers=auth['refresh_token'])
    assert response.status_code == 200
    assert response.json['status'] == 'success'

    # checks tokens created
    access_token_decoded = decode_token(response.json['data']['access_token'])
    assert access_token_decoded['identity'] == 'test'

    # checks for tokens in the database
    from app.model import Token
    assert session.query(Token).filter_by(jti=access_token_decoded['jti'],
                                          user_identity='test').first()


def test_auth_refresh_an_invalid_token_returning_422_status_code(client):
    """
    GIVEN a Flask application
    WHEN the '/auth/login' URL is requested (POST) with an invalid token
    THEN check the response HTTP 402 response
    """

    response = client.post('/auth/refresh',
                           content_type='application/json',
                           headers={'Authorization': 'Bearer invalid-token'})
    assert response.status_code == 422
    assert response.json['msg'] == 'Not enough segments'
