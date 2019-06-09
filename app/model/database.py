"""This module provides means to perform operations on the database
using the SQLAlchemy library."""


import click

from flask import Flask
from flask.cli import with_appcontext

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


Base = None
engine = None
db_session = None


def init(app: Flask) -> None:
    """This function initialize the SQLAlchemy ORM, providing a session
    and command line to create the tables in the database.
    """

    global Base, engine, db_session
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    # creating a new session
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))

    # The declarative extension in SQLAlchemy allows to define
    # tables and models in one go, that is in the same class
    Base = declarative_base()
    Base.query = db_session.query_property()

    # attach the shutdown_session function to be execute when a request ended.
    app.teardown_appcontext(shutdown_session)

    # adding the init_db_command to line command input
    app.cli.add_command(init_db_command)


def shutdown_session(exception=None) -> None:
    """Remove the session by send it back to the pool."""

    db_session.remove()


def init_db(test=None) -> None:
    """Import all modules here that might define models so that
    they will be registered properly on the metadata.
    """

    import app.model.models
    Base.metadata.create_all(bind=engine)


def drop_db() -> None:
    """Remove all table from database."""

    db_session.remove()
    import app.model.models
    Base.metadata.drop_all(bind=engine)


@click.command('init-db')
@with_appcontext
def init_db_command() -> None:
    """This function is executed through the 'init-db' line
    commando, than it creates the tables into the database."""

    init_db()
    click.echo('Initialized the database.')
