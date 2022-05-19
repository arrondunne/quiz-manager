import sqlite3
from flask import Flask, g, request, session, url_for, redirect, flash, render_template
from werkzeug.security import check_password_hash

#import click
#from flask import current_app, g
#from flask.cli import with_appcontext

# Database Location


DATABASE = 'quiz_manager.db'

app = Flask(__name__)


def init_db():
    db = get_db()

    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('quiz_manager.db')
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@app.before_first_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None

    else:
        db = get_db()
        g.user = db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()


@app.route('/')
def hello():
    init_db()
    get_db()
    return render_template('base.html')


@app.route('/login', methods=('GET', 'POST'))
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


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


app.run()