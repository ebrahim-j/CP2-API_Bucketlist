import os
from flask_script import Manager, prompt_bool # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from app import models

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

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


if __name__ == '__main__':
    manager.run()
