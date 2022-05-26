import functools
from flask import Flask, g, request, session, url_for, redirect, flash, render_template, Blueprint
from werkzeug.security import check_password_hash
from application.db import get_db

"""
    Module which contains all the flask functions, which contains the logic and endpoints for the front-end UI.
"""

# Create a flask blueprint for the endpoints
bp = Blueprint('quiz_manager', __name__)


def login_required(view):
    """
        Function that creates decorator requiring a user to be logged-in. The original view is passed in and wrapped in
        a new view function. The new function checks is a user is loaded. If a user is logged int, the original view is
        called and continues normally. If a user is not logged-in, the user will be redirected to the login page.
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('quiz_manager.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/')
@login_required
def home():
    """
        The Home page. This is on the root index and shows the user all the quizzes stored. The database connection is
        made and then a SQL query is exected to select all entries in the quiz table. The quizzes are then passed into
        the home.html template which is rendered using flask to the user. A user must be logged-in.
    """
    db = get_db()
    quizzes = db.execute("SELECT * FROM quizzes;").fetchall()

    return render_template('home.html', quizzes=quizzes)


@bp.route('/<quiz_id>/questions')
@login_required
def questions(quiz_id):
    """
        The Questions page. After clicking on a quiz from the Home page, the user will be redirected here with the
        quiz_id in the URL and passed into the function. This page will show users all the questions for the selected
        quiz. The database connection is made and then a SQL query is executed to select all entries in the question
        table for the given quiz_id. The questions are then passed into the questions_page.html template which is
        rendered using flask to the user. A user must be logged-in.
    """
    db = get_db()
    questions = db.execute("SELECT * FROM questions WHERE quiz_id = ?", quiz_id).fetchall()

    return render_template('questions_page.html', questions=questions)


@bp.route('/<question_id>/answers')
@login_required
def answers(question_id):
    """
        The Answers page. After clicking on a question from the Questions page, the user will be redirected here with the
        question_id in the URL and passed into the function. This page will show users all the answers for the selected
        question. The database connection is made and then a SQL query is executed to select all entries in the answers
        table for the given question_id. The answers are then passed into the answers_page.html template which is
        rendered using flask to the user. A user must be logged-in.
    """
    db = get_db()
    answers = db.execute("SELECT * FROM answers WHERE question_id = ?", question_id).fetchall()

    return render_template('answers_page.html', answers=answers)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
        The Login page. Users will be directed here if they are not logged-in.
        The page consists of a form for users to login and supports GET and POST requests.
    """

    # If a user is submitting a form as a POST request, check the username and password, and if correct, log the user in
    if request.method == 'POST':
        # Get data from the submitted form
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        # If any fields are empty, create an error
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        # Get user data from the database for the user using SQL statement
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        # If username is not in database, create an error
        if user is None:
            error = 'Incorrect username'
        # If the password does not match the stores password, after hashing it, create an error
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        # If there are no errors, create a user session using flask and redirect the user to the Home page
        if error is None:
            session.clear()
            session['user_id'] = user['user_id']

            return redirect(url_for('home'))

        # If there are errors, show them to the user
        flash(error)

    # If this is a GET request, show the user the login.html template, loaded using flask
    return render_template('login.html')


@bp.route('/logout')
def logout():
    """
        The Logout page. Users will be directed here if they click the logout button.
        The user sessions will be cleared and then the user will be redirected to the Login page.
    """
    session.clear()
    return redirect(url_for('quiz_manager.login'))


@bp.before_app_request
def load_logged_in_user():
    """
        This function is user to get the user session, if there is one. It gets the user_id from the flask sessions,
        and then if there is a user, gets the user data from the database and assigns it to the global flask variable, g
    """
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()


