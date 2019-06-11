"""Tests for the HTTP REST API base."""

def test_index_route(client):
    response = client.get('/')
    assert response.data == b'The server is runing!'


def test_not_found_exception(client):
    response = client.get('/xxxxxxxxx')
    assert response.status_code == 404
    assert response.json['status'] == 'error'
    assert response.json['message'] == 'not Found'