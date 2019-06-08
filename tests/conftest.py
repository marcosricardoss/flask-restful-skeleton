"""This module is responsible to initial configuration of
the test. On that, it creates fixtures to get an application
instance and simulates interactions over it.
"""

import os
import pytest

from dotenv import load_dotenv

from app import create_app
from app.model.database import init_db, clean_db, shutdown_session


@pytest.fixture
def app():
    """ Create a application instance from given settings.

    Returns:
        flask.app.Flask: The application instance
    """

    # loading the test\.env to environment
    load_dotenv()

    # app instance
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL')
    })

    # creating the database tables
    with app.app_context():        
        init_db()

    yield app

    with app.app_context():        
        clean_db()
        init_db()        
        

@pytest.fixture
def client(app):
    """Create a client with app.test_client() using app fixture.
    Tests will use the client to make requests to the application

    Parameters:
        app (flask.app.Flask): The application instance.

    Returns:
        FlaskClient: A client to allow make requests to the application.
    """

    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a runner with app.test_cli_runner() using app fixture, that
    can call the Click commands registered with the application.

    Parameters:
        app (flask.app.Flask): The application instance.

    Returns:
        flask.testing.FlaskCliRunner: A client to allow make requests to the application.
    """

    return app.test_cli_runner()
