"""This package is a solution to the problem used by the Olist
company to evaluate the candidate skills.

Original repository: https://github.com/olist/work-at-olist

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
    registes_blueprints(app)

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

    from .model import database
    database.init(app)


def registes_blueprints(app: Flask) -> None:
    """Registes the blueprint to the application.

    Parameters:
        app (flask.app.Flask): The application instance Flask that'll be running
    """

    from .blueprint import index, users
    app.register_blueprint(index.bp)
    app.register_blueprint(users.bp)
