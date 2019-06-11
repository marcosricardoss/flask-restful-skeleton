""" This module contains tests related to factory function """

import os

from dotenv import load_dotenv
from app import create_app


def test_config_not_testing():
    load_dotenv()
    config = {'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL')}
    assert not create_app(config).testing


def test_config_testing():
    load_dotenv()
    config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL')
    }
    assert create_app(config).testing
