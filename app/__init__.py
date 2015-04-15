# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, AnonymousUserMixin

from config import _basedir

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)


class UserAnonymous(AnonymousUserMixin):
    id = None

    def is_admin(self):
        return False

lm = LoginManager()
lm.init_app(app)
lm.anonymous_user = UserAnonymous
lm.login_view = 'user_login'


@lm.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
