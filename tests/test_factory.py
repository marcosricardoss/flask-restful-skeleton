""" This module contains tests related to factory function """

import os

from dotenv import load_dotenv
from app import create_app


def test_config():
    load_dotenv()

    config_not_testing = {'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL')}
    assert not create_app(config_not_testing).testing

    config_testing = {'TESTING': True, 'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL')}
    assert create_app(config_testing).testing


def test_index(client):
    response = client.get('/')
    assert response.data == b'The server is runing!'
