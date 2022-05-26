import os
import tempfile
import pytest
from application import create_app
from application.db import get_db, init_db

"""
    Module containing PyTest fixtures. Fixtures are reusable piueces of code that can be used in tests for steps which
    happen repeatedly
"""

# Read the test_data.sql file and assign it to a variable for later use
with open(os.path.join(os.path.dirname(__file__), 'test_data.sql'), 'rb') as f:
    _test_data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """
        A fixture which creates an instance of the applivcation in testing mode and fills the database with the test
        data. This application instance is then yielded to the function that called the fixture.
    """

    # Create temporary file so database path is not overridden
    db_fd, db_path = tempfile.mkstemp()

    # Initialise the application in testing mode
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        # Initialise the database
        init_db()
        # Execute the SQL to add test_data to the database
        get_db().executescript(_test_data_sql)

    # Yield the application back to the function that called it
    yield app

    # Close the temporary files
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """
        Fixture so that tests can call this client and make requests to the application without needing to run them on
        the server
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
        Fixture that can call the command line interface
    """
    return app.test_cli_runner()


class AuthActions(object):
    """
        Fixture that allows a user to login and logout as the test user, which was added to the database in the app
        fixture
    """
    def __init__(self, client):
        # initialise the _client attribute with the client object
        self._client = client

    def login(self, username='test', password='test'):
        # log the user in using test data
        return self._client.post(
            '/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        # log the user out
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    """
        Fixture which calls the AuthActions fixture
    """
    return AuthActions(client)
