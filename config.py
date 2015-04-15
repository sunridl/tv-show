import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

CSRF_ENABLED = True
CSRF_SESSION_KEY = "NB7yJaMEyI8OGsFbrZ66B48S"

SECRET_KEY = 'NB7yJaMEyI8OGsFbrZ66B48S'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')

ROOT_DIR = _basedir
