"""Tests for the HTTP REST API base."""


def test_access_index_url_returning_200_status_code(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'The server is runing!'


def test_acces_an_inexistent_url_returning_404_status_code(client):
    response = client.get('/xxxxxxxxx')
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'not Found'


def test_to_access_a_protected_url_returning_200_status_code(client, auth):
    endpoint = '/users'
    response = client.get(endpoint, headers=auth['access'])
    assert response.status_code == 200


def test_to_access_a_protected_url_returning_401_status_code(client):
    endpoint = '/users'
    response = client.get(endpoint)
    assert response.status_code == 401
