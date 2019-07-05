"""This module is responsible to initial configuration of the test. On that, 
it creates fixtures to get an applicationinstance and simulates interactions over it.
"""


import os
import pytest
import dotenv

from app import create_app


def init_db() -> None:
    """Import all modules here that might define models so that
    they will be registered properly on the metadata.
    """

    import app.model.models
    from app.database import Base, engine
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Remove all table from database."""

    from app.database import Base, engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def app(request):
    """ Create a application instance from given settings.

    Parameters:
        request (FixtureRequest): A request for a fixture from a test or fixture function

    Returns:
        flask.app.Flask: The application instance
    """

    # loading the .env to environment
    dotenv.load_dotenv()

    # app instance
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL')
    })

    # add to the scope
    ctx = app.app_context()
    ctx.push()

    def teardown():
        drop_db()
        init_db()
        ctx.pop()

    init_db()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='function')
def client(app):
    """Create a client with app.test_client() using app fixture.
    Tests will use the client to make requests to the application

    Parameters:
        app (flask.app.Flask): The application instance.

    Returns:
        FlaskClient: A client to allow make requests to the application.
    """

    return app.test_client()


@pytest.fixture(scope='function')
def session(app, request):
    """Creates a new database session for a test.

    Parameters:    
        app (flask.app.Flask): The application instance.
        request (FixtureRequest): A request for a fixture from a test or fixture function

    Returns:
        db_session: a SLQAlchmey Session object.
    """

    from app.database import db_session

    def teardown():
        db_session.remove()

    request.addfinalizer(teardown)
    return db_session


@pytest.fixture(scope='function')
def runner(app):
    """Create a runner with app.test_cli_runner() using app fixture, that
    can call the Click commands registered with the application.

    Parameters:
        app (flask.app.Flask): The application instance.

    Returns:
        flask.testing.FlaskCliRunner: A client to allow make requests to the application.
    """

    return app.test_cli_runner()


@pytest.fixture
def auth(app, request):
    """Creates HTTP authorization header for a basic authentication.

    Parameters:    
        app (flask.app.Flask): The application instance.
        request (FixtureRequest): A request for a fixture from a test or fixture function

    Returns:
       headers: a dictionary with HTTP authorization header for a basic authentication
    """

    import base64
    from app.model import User
    from werkzeug.security import generate_password_hash
    from app.database import db_session

    user = db_session.query(User).filter_by(username='test').first()

    if not user:
        user = User()
        user.username = 'test'
        user.password = generate_password_hash('test')

        db_session.add(user)
        db_session.commit()

    encoded = base64.b64encode(b'test:test').decode('utf-8')
    headers = {'Authorization': 'Basic ' + encoded}

    return headers
