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
        'DATABASE': database_file_path,
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