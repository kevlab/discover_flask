from flask import Flask, render_template, redirect, url_for, session, flash
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
# export APP_SETTINGS="config.DevelopmentConfig"
# printenv APP_SETTINGS
# to set and see enviroment variables in terminal shell
# from app import app, print app.config in python shell to verify
# environment variables can be stored with virtualenvwrapper and auto-loaded
# isntall virtualenvwrapper globally!, not within a venv

db = SQLAlchemy(app)
from models import *

from project.users.views import users_blueprint
app.register_blueprint(users_blueprint)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first!')
            return redirect(url_for('users.login'))
    return wrap


@app.route('/')
@login_required
def home():
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', posts=posts)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run()
