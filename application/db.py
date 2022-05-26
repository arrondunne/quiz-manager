import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

"""
    Module containing all the databse functions, which can be called from other modules in the application
"""


def get_db():
    """
        It there is no database connection on the flask global variable g, a connection is established to the database
        and returned as part of g
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """
        The database is taken off the flask global variable g and the connection is closed
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
        The database is initialized from the schema.sql file. A database connection is made, then the file is loaded
        and executed. Any tables in the database are deleted and then new tables are created according to the schema
        in the design.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def add_data_db():
    """
        Sample data from the file data.sql is added to the database. A database connection is made, then the file is
        loaded and executed. Sample data is added to the tables in the database
    """
    db = get_db()

    with current_app.open_resource('data.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
        Command line function to initialise the database using init-db on the command line, which calls init_db.py.
        A response is also written to the console for user feedback
    """
    init_db()
    click.echo('Initialized the database.')


@click.command('add-data-db')
@with_appcontext
def add_data_db_command():
    """
        Command line function to add data to the database using add-data-db on the command line, which calls
        add_data_db.py. A response is also written to the console for user feedback
    """
    add_data_db()
    click.echo('Populated the database with new data.')


def init_app(app):
    """
        Assigns the functions to the be callable
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_data_db_command)