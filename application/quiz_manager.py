import functools
import json
import sqlite3
import pandas as pd
from flask import Flask, g, request, session, url_for, redirect, flash, render_template, Blueprint
from werkzeug.security import check_password_hash, generate_password_hash

from application.db import get_db


bp = Blueprint('quiz_manager', __name__)


@bp.route('/')
def home():
    db = get_db()
    quizzes = db.execute("SELECT * FROM quizzes;").fetchall()

    return render_template('home.html', quizzes=quizzes)


@bp.route('/<quiz_id>/questions')
def questions(quiz_id):
    db = get_db()
    questions = db.execute("SELECT * FROM questions WHERE quiz_id = ?", quiz_id).fetchall()

    return render_template('questions_page.html', questions=questions)


@bp.route('/<question_id>/answers')
def answers(question_id):
    db = get_db()
    answers = db.execute("SELECT * FROM answers WHERE question_id = ?", question_id).fetchall()

    return render_template('answers_page.html', answers=answers)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_id'] = user['user_id']

            return redirect(url_for('home'))

        flash(error)

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('quiz_manager.login'))

        return view(**kwargs)

    return wrapped_view