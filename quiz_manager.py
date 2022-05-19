import json
import sqlite3
import pandas as pd
from flask import Flask, g, request, session, url_for, redirect, flash, render_template
from werkzeug.security import check_password_hash, generate_password_hash

#import click
#from flask import current_app, g
#from flask.cli import with_appcontext

# Database Location
DATABASE = 'quiz_manager.db'

app = Flask(__name__)

app.config.from_mapping(SECRET_KEY = 'dev')

def row_to_dict(rs):
    """
    Takes a SQL results list (from a fetchall command) and converts it into a dict
    """
    list = []
    for row in rs:
        row_dict = {}
        for col in row.keys():
            row_dict.update({col: row[col]})
        list.append(row_dict)
    json.dumps(list, indent=4)
    return list

def init_db():
    db = get_db()

    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    add_users_db()
    add_quizzes_db()


def add_users_db():
    data = pd.read_csv('users.csv')
    df = pd.DataFrame(data)
    db = get_db()
    for index, row in df.iterrows():
        db.execute("INSERT INTO users (username, password, permission) VALUES (?, ?, ?)",
                   (row['username'], generate_password_hash(row['password']), row['permission']))
        db.commit()


def add_quizzes_db():
    with open ("testquiz.json") as read_file:
        file = json.load(read_file)

        db = get_db()

        db.execute("INSERT INTO quizzes (title, description) VALUES (?, ?)",
                   (file['Title'], file['Description']))
        db.commit()
        quiz_id = row_to_dict(db.execute(f"SELECT quiz_id FROM quizzes WHERE title='{file['Title']}';").fetchall())
        for question in file["Questions"]:
            db.execute("INSERT INTO questions (quiz_id, question) VALUES (?, ?)", (quiz_id, question["Question"]))
            db.commit()
            question_id = row_to_dict(db.execute(f"SELECT question_id FROM questions WHERE question='{question['Question']}';").fetchall())
            for answer in question["Answers"]:
                db.execute("INSERT INTO answers (question_id, answer) VALUES (?, ?)", (question_id, answer))
        db.commit()


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
def home():
    init_db()
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