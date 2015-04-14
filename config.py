import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

CSRF_ENABLED = True
CSRF_SESSION_KEY = "NB7yJaMEyI8OGsFbrZ66B48S"

SECRET_KEY = 'NB7yJaMEyI8OGsFbrZ66B48S'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

ROOT_DIR = basedir
