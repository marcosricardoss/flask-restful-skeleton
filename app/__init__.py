"""This package is Flask HTTP REST API Template template that already has the database bootstrap
implemented and also all feature related with the user authentications.

Application features:
    Python 3.7
    Flask
    PEP-8 for code style

This module contains the factory function 'create_app' that is
responsible for initializing the application according
to a previous configuration.
"""


import os

from flask import Flask
from flask_jwt_extended import JWTManager

def create_app(test_config: dict = None) -> Flask:
    """This function is responsible to create a Flask instance according
    a previous setting passed from environment. In that process, it also
    initialise the database source.

    Parameters:
        test_config (dict): settings coming from test environment

    Returns:
        flask.app.Flask: The application instance
    """

    app = Flask(__name__, instance_relative_config=True)    
    
    load_config(app, test_config)
    
    init_instance_folder(app)
    init_database(app)
    init_blueprints(app)
    init_commands(app)
    init_jwt_manager(app)    

    return app


def load_config(app: Flask, test_config: dict) -> None:
    """Load the application's config

    Parameters:
        app (flask.app.Flask): The application instance Flask that'll be running
        test_config (dict):
    """

    if not test_config:
        if os.environ.get('FLASK_ENV') == 'development':
            # load config object containing the development environment settings
            app.config.from_object('app.config.Development')
        else:
            # load config object containing the production environment settings
            app.config.from_object('app.config.Production')
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)


def init_instance_folder(app: Flask) -> None:
    """Ensure the instance folder exists.

    Parameters:
        app (flask.app.Flask): The application instance Flask that'll be running
    """

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


def init_database(app) -> None:
    """Responsible for initializing and connecting to the database
    to be used by the application.

    Parameters:
        app (flask.app.Flask): The application instance Flask that'll be running
    """

    from .database import init
    init(app)


def init_blueprints(app: Flask) -> None:
    """Registes the blueprint to the application.

    Parameters:
        app (flask.app.Flask): The application instance Flask that'll be running
    """

    # error handlers
    from .blueprint.handler import register_handler
    register_handler(app)

    # error Handlers
    from .blueprint import index, users, auth
    app.register_blueprint(index.bp)
    app.register_blueprint(users.bp)
    app.register_blueprint(auth.bp)

def init_commands(app):
    from app.commands import register_commands
    register_commands(app)

def init_jwt_manager(app):
    from .authentication import init
    jwt = JWTManager(app)
    init(jwt)