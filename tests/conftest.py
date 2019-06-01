import os
import tempfile

import pytest
from app import create_app
from app.model.database import DBFactory


@pytest.fixture
def app():

    database_fd, database_file_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,        
        'HOST': "127.0.0.1",
        'PORT': 3320,
        'USER': "root",
        'PASSWORD': "123",
        'DATABASE': "olist_test"
    })    
    
    with app.app_context():
        DBFactory().create()        
        
    yield app

    os.close(database_fd)
    os.unlink(database_file_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()