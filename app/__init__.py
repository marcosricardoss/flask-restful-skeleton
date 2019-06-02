import os

from flask import Flask

def create_app(test_config=None):
    """Create and configure the app."""
    
    app = Flask(__name__, instance_relative_config=True)    
    load_config(app, test_config) 
    init_instance_folder(app) 
    init_database(app)
    registes_blueprints(app)
        
    return app


def load_config(app, test_config): 
    """Load the application's config"""    

    if not test_config:
        if os.environ.get('APP_SETTINGS'):
            # load object config passed passed through 'APP_SETTINGS' environment variable
            app.config.from_object(os.environ.get('APP_SETTINGS'))
        else:
            app.config.from_object('app.config.Production')     
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


def init_instance_folder(app):
    """Ensure the instance folder exists."""

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass        


def init_database(app):
    """Responsible for initializing and connecting 
    to the database to be used by the application.
    """

    from .model import database
    database.init_app(app)       


def registes_blueprints(app):
    """Registes the blueprint to the application."""

    from .blueprint import index
    app.register_blueprint(index.bp)