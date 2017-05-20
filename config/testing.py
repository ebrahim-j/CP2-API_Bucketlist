
import os
TESTING = True
DEBUG = True
SECRET_KEY = 'noLifeWithoutTracebacks'
# SQLALCHEMY_DATABASE_URI = "postgresql://localhost/test_db"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../tests.db')

