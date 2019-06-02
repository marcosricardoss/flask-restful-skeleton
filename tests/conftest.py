import os
import tempfile

import pytest
from dotenv import load_dotenv
from app import create_app
from app.model.database import DBFactory


@pytest.fixture
def app():
    load_dotenv()
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': os.environ.get('DATABASE_URL')
    })

    with app.app_context():
        DBFactory().create()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
