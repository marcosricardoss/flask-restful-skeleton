"""This module provides means to perform operations on the database using the SQLAlchemy library."""

import click

from flask import Flask
from flask import current_app, g
from flask.cli import with_appcontext

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = None


class Database:
    """Class used to connect to application's configured database."""

    def __init__(self) -> None:
        global Base
        Base = declarative_base()
        self.___init_database()

    def ___init_database(self) -> None:
        """Initialize the database.

        This method initialize a session make and a sqlalchemy engine.
        Then it use a internal factory function make possible to
        use declarative class definitions
        """

        self.__engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
        # creating a new session
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def create(self) -> None:
        """ Import all modules here that might define models so that
        they will be registered properly on the metadata.
        """
        import app.model.persistent_objects
        Base.metadata.create_all(bind=self.__engine)

    def get_base(self) -> Base:
        """Provides the base class for declarative class definitions.

        Returns:
            Base: A SQLAlchemy base class
        """
        return Base

    def get_session(self) -> sqlalchemy.orm.session.Session:
        """Provides the active current session and add it to the special object g.

        Returns:
            self.__session: A SQLAlchemy Session object
        """

        click.echo(self.__session)

        if 'session' not in g:
            g.session = self.__session
        return g.session

    @staticmethod
    def shutdown_session(exception=None) -> None:
        """Checkig for a session in the g object and close it."""

        session = g.pop('session', None)
        if session is not None:
            session.close()


@click.command('init-db')
@with_appcontext
def init_db_command() -> None:
    """Clear the existing data and create new tables."""

    Database().create()
    click.echo('Initialized the database.')


def init_app(app: Flask) -> None:
    """Register database functions with the Flask app. This is called by
    the application factory.
    """

    # attach the static shutdown_session to be execute when a request is ended.
    app.teardown_appcontext(Database.shutdown_session)
    # adding the init_db_command to line command input
    app.cli.add_command(init_db_command)
