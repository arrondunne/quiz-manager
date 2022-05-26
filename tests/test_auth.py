import pytest
from flask import g, session

"""
    Module with tests that test the Login page
"""


def test_login_required(client, auth):
    """
        GIVEN a user not logged-in
        WHEN the user goes to the Home page URL
        THEN the user shall be directed to the Login page
    """
    response = client.get('/')

    assert response.headers['Location'] == '/login'


def test_login(client, auth):
    """
        GIVEN A registered user
        WHEN a user loads the login page URL and logs in
        THEN the user shall be shown the home page and have a session with that username
    """
    assert client.get('/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username'),
    ('test', 'a', b'Incorrect password'),
))
def test_login_validate_input(auth, username, password, message):
    """
        GIVEN a user on the login page
        WHEN a user enters incorrect details
        THEN an error message shall be returned
    """
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    """
        GIVEN a logged in user
        WHEN the user logs-out
        THEN the user session shall be ended and directed to the login page
    """
    auth.login()

    with client:
        response = auth.logout()
        assert response.headers["Location"] == "/login"
        assert 'user_id' not in session