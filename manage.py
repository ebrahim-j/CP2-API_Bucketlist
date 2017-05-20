import os
from app import create_app, db


from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from flask import jsonify


# make Flask application from app factory
app = create_app(os.getenv('APP_SETTINGS') or 'development')
with app.app_context():
    from app.models import User, Item, Bucketlist
# initialise manager class
manager = Manager(app)
# initialise migrate class
migrate = Migrate(app, db)



manager.add_command('db', MigrateCommand)


# @manager.command
# def test():
#     """Run the unit tests."""
#     pass


@manager.command
def initdb():
    """ initialise the database with creation of tables """
    db.create_all()
    db.session.commit()
    print("......Done")


@manager.command
def dropdb():
    """ delete all the data in the database and destroy all the tables """
    if prompt_bool("Are you sure you want to destroy all your data"):
        db.drop_all()
        print("Byebye db :'(")

if __name__ == "__main__":
    manager.run()
