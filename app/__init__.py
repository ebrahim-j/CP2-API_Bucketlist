import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_set
# from instance.config import app_config

app = Flask(__name__)
db = SQLAlchemy()


def create_app(config_name):
    """
        Create an application instance.
        This function acts as a factory function that
        can create different flask app instances based
        on the configuration settings it is passed
    """
    app = Flask(__name__)

    # import configuration for the application from instance folder
    # app.config.from_object(app_config[config_name])
    # app.config.from_pyfile('config.py')

    # cfg = os.path.join(os.getcwd(), 'config', config_name + '.py')
    # app.config.from_pyfile(cfg)

    app.config.from_object(config_set[config_name])
    config_set[config_name].init_app(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize flask extensions on the application instance
    db.init_app(app)

    # register API blueprints
    from .bucketlist import bucketlist_blueprint # as api_blueprint
    from .auth import auth_blueprint # as auth_blueprint
    app.register_blueprint(bucketlist_blueprint, url_prefix='/api')
    app.register_blueprint(auth_blueprint, url_prefix="/api")

    return app


