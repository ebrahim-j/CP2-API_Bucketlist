import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'tracebackErrorsAreLife'

# SQLALCHEMY_DATABASE_URI = "postgresql://localhost/flask_api"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../database.sqlite3')
