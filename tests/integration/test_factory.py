""" This module contains tests related to factory function """

import os

from dotenv import load_dotenv
from app import create_app


def test_without_config():
    """
    GIVEN the create_app() factory function
    WHEN an app created with empty config
    THEN check test environment execution
    """

    load_dotenv()
    config = {}
    assert not create_app(config).testing


def test_with_test_config_testing():
    """
    GIVEN the create_app() factory function
    WHEN an app created with config for testing environment
    THEN check test environment execution
    """

    load_dotenv()
    config = {
        'TESTING': True,
        'DEBUG': True,
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL')
    }
    app = create_app(config)
    assert app.testing
    assert app.debug
    assert app.config.get(
        'SQLALCHEMY_DATABASE_URI') == os.environ.get('DATABASE_URL')


def test_with_development_config():
    """
    GIVEN the create_app() factory function
    WHEN an app created with config for development environment
    THEN check test environment execution
    """

    load_dotenv()
    config = {
        'FLASK_ENV': 'development',
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL')
    }
    app = create_app(config)
    assert not app.testing
    assert app.debug
    assert app.config.get('JWT_BLACKLIST_ENABLED') == True
    assert app.config.get('JWT_BLACKLIST_TOKEN_CHECKS') == [
        'access', 'refresh']
    assert app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS') == False
    assert app.config.get('SECRET_KEY') == 'dev'
    assert app.config.get('JWT_SECRET_KEY') == 'dev'
    assert app.config.get(
        'SQLALCHEMY_DATABASE_URI') == os.environ.get('DATABASE_URL')


def test_with_production_config():
    """
    GIVEN the create_app() factory function
    WHEN an app created with config for production environment
    THEN check test environment execution
    """

    load_dotenv()
    config = {
        'FLASK_ENV': 'production',
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL')
    }
    app = create_app(config)
    from app.config import Production, Development
    assert not app.testing
    assert not app.debug
    assert app.config.get('JWT_BLACKLIST_ENABLED') == True
    assert app.config.get('JWT_BLACKLIST_TOKEN_CHECKS') == [
        'access', 'refresh']
    assert app.config.get('SQLALCHEMY_TRACK_MODIFICATIONS') == False
    assert app.config.get('SECRET_KEY') == Production.SECRET_KEY
    assert app.config.get('JWT_SECRET_KEY') == Production.JWT_SECRET_KEY
    assert app.config.get(
        'SQLALCHEMY_DATABASE_URI') == os.environ.get('DATABASE_URL')
