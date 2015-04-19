#!env/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import random
import datetime
import readline

from pprint import pprint as p

from flask import *
from sqlalchemy.exc import SQLAlchemyError

from app import *

from app.models import *
from app import views
from app.forms import *


def create_admin():
    """Adds User('Admin', '123456', 'admin@nonemail.com', is_admin=True) to database"""
    admin = User('Admin', '123456', 'admin@nonemail.com', is_admin=True)
    admin.active = True
    try:
        db.session.add(admin)
        db.session.commit()
    except SQLAlchemyError as e:
        print(e)
        db.session.rollback()

try:
    import IPython
    IPython.embed()
except ImportError:
    os.environ['PYTHONINSPECT'] = 'True'

ctx = app.test_request_context()
ctx.push()
app.preprocess_request()
