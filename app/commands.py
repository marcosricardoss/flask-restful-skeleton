import click
from flask.cli import with_appcontext


def register_commands(app):
    """Add commands to the line command input.

    Parameters:    
        app (flask.app.Flask): The application instance.
    """

    app.cli.add_command(add_user_command)


@click.command('user')
@click.argument('username')
@click.argument('password')
@with_appcontext
def add_user_command(username: str, password: str) -> None:
    """This function is executed through the 'user' line command.
    e.g.: flask user demo demo

    Parameters:
        username (str): The username of the user.
        password (str): The password of the user.
    """

    add_user(username, password)


def add_user(username: str, password: str) -> None:
    """Create a new user.

    Parameters:
        username (str): The username of the user.
        password (str): The password of the user.
    """

    from app.model import User
    from app.model import UserRepository

    user_repository = UserRepository()
    user = User(username=username, password=password)

    is_invalid = user_repository.is_invalid(user)
    if not is_invalid:
        user_repository.save(user)
        click.echo('User created.')
    else:
        click.echo('Could not validate the user:')
        for i in is_invalid:
            key = list(i.keys())[0]
            click.echo("{}: {}".format(key, i[key]))
