import os
import tempfile

import pytest
from app import create_app
from app.model.database import DBFactory


@pytest.fixture
def app():   
    postgresql_uri = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        "postgres", 
        "123", 
        "127.0.0.1", 
        15432, 
        "olist_test"
    ) 

    app = create_app({
        'TESTING': True,                
        'SQLALCHEMY_DATABASE_URI': postgresql_uri
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