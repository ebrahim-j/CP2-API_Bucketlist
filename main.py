import os
from app import create_app, db

if __name__ == '__main__':
    config_name = os.getenv('APP_SETTINGS') # config_name = "development"
    app = create_app(config_name or 'development')
    with app.app_context():
        db.create_all()
    app.run()
