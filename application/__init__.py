import os
from flask import Flask
from . import db
from . import quiz_manager


def create_app(test_config=None):
    """
        Creates a flask instance of the application. This function is a factory which configures the flask app and
        returns an initialised application. test_config may be passed in for running tests, otherwise, for normal
        development, it will be None.
    """

    # Crate a Flask instance
    app = Flask(__name__, instance_relative_config=True)

    # Configure the app with a secret key and the database path
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'quiz_manager.db')
    )

    # Override the defasult configurations with values taken from config.py, if it exists. This can be used to override
    # the secret key when deploying
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    # If test_config is passed in, use this
    else:
        app.config.from_mapping(test_config)

    # Creates the app folder is created. Flask doesnt create this automoatically but it is necessary
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialise the database functions from db.py
    db.init_app(app)

    # Register the blueprint from quiz_manager.py to the app instance so they can be used
    app.register_blueprint(quiz_manager.bp)

    # Create a URL that directs the 'home' function to the root URL
    app.add_url_rule('/', endpoint='home')

    # Return the created and configured application
    return app
