""" This module contains tests related to factory function """

from app import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_index(client):
    response = client.get('/')
    assert response.data == b'The server is runing!'
