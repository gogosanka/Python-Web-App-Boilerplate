#initialize the app and database instances
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#initialize authentication packages
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

#initialize the controllers and db models
from smh import views
from smh.models.models import *

#initialize other routes blueprints
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')