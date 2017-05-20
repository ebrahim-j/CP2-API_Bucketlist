import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    This holds the default configuration settings that will be inherited
    for the software environment setup
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'check_point_rules'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    """
    The development environment used throughout setup
    """
    DEBUG = True
    # the following configuration defines postgres database for developmement
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = ('postgresql://
                                             bucketlist:bucketlist@localhost
                                             /bucketlist')
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.db')


class Testing(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.db')

config_set = {
    "development": Development,
    "testing": Testing,
    "default": Development
    }

expiry_time = 3600


# import os

# class BaseConfig:
#     """Base configuration."""
#     DEBUG = False
#     CSRF_ENABLED = True
#     SECRET_KEY = os.getenv('SECRET')
#     # BCRYPT_LOG_ROUNDS = 13
#     SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

# class DevelopmentConfig(BaseConfig):
#     """Development configurations"""
#     DEBUG = True
#     # BCRYPT_LOG_ROUNDS = 4


# class TestingConfig(BaseConfig):
#     """Testing configuration"""
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '../tests.db')
#     DEBUG = True
#     # BCRYPT_LOG_ROUNDS = 4

# class ProductionConfig(BaseConfig):
#     """Production configuration"""
#     DEBUG = False
#     TESTING = False

# app_config = {
#     'development': DevelopmentConfig,
#     'testing': TestingConfig,
#     'production': ProductionConfig,
# }
