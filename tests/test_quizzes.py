import pytest
from application.db import get_db


def test_home(client, auth):
    """
        GIVEN a logged-in user and test data
        WHEN the user goes to the Home Page URL
        THEN the user shall be shown the Home Page and Quiz data
    """
    auth.login()
    response = client.get('/')
    assert response.status_code == 200
    assert b'Log Out' in response.data
    assert b'Maths Quiz' in response.data
    assert b'Home Page' in response.data


def test_quiz(client, auth):
    """
        GIVEN a logged-in user and test data
        WHEN the user selects a quiz
        THEN the user shall be shown the question page for that quiz
    """
    auth.login()
    response = client.get('/1/questions')
    assert response.status_code == 200
    assert b'What is 1 + 1?' in response.data


def test_question(client, auth):
    """
        GIVEN a logged-in user and test data
        WHEN the user selects a question
        THEN the user shall be shown the answers page for that question
    """
    auth.login()
    response = client.get('/1/answers')
    assert response.status_code == 200
    assert b'1' in response.data


