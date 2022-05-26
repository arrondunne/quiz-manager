from application import create_app

"""
    A  Module for testing the app creation/factory
"""


def test_config():
    """
        GIVEN a instance of the application
        WHEN a second instance of the application is created
        THEN both instances shall be the same
    """
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing