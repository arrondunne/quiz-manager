import pytest
import sqlite3
from application.db import get_db

"""
    A Module for testing the database functions
"""


def test_get_db(app):
    """
        GIVEN a initialised database with test data
        WHEN the database is retrieved using get_db
        THEN subsequent uses of get_db should return the same connection
    """
    with app.app_context():
        db = get_db()
        assert db is get_db()


def test_close_db(app):
    """
        GIVEN a initialised database with test data
        WHEN an error is raised and the application closes
        THEN the database connection should be closed
    """
    with app.app_context():
        db = get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    """
        GIVEN a recorder (monkeypatch) on the init_db function
        WHEN the init-db terminal command is executed
        THEN the init_db function shall be executed, and recorded by the listener
    """
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('application.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'Initialized' in result.output
    assert Recorder.called