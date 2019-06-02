import os
import tempfile

import pytest
from app import create_app
from app.model.database import DBFactory


@pytest.fixture
def app():   
    app = create_app({
        'TESTING': True,        
        'HOST': "127.0.0.1",
        'PORT': 15432,
        'USER': "postgres",
        'PASSWORD': "123",
        'DATABASE': "olist_test"        
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