# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
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


@app.template_filter('datetime')
def format_datetime(value, format='%d.%m.%Y %H:%M'):
    return datetime.strftime(value, format)


@app.template_filter('timedelta')
def format_timedelta(value, format='%H h %M min'):
    value = int(value.total_seconds())
    secs = value % 60
    mins = (value / 60) % 60
    hours = (value / 60 / 60) % 24
    return datetime(year=2000, month=1, day=1, hour=hours, minute=mins, second=secs).strftime(format)
