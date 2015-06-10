from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config.from_object(os.environ['APP_SETTINGS'])
# export APP_SETTINGS="config.DevelopmentConfig"
# printenv APP_SETTINGS
# to set and see enviroment variables in terminal shell
# from app import app, print app.config in python shell to verify
# environment variables can be stored with virtualenvwrapper and auto-loaded
# isntall virtualenvwrapper globally!, not within a venv

db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.home.views import home_blueprint


app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)
