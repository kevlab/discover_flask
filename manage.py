from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import os

from app import app, db

app.config.from_object(os.environ['APP_SETTINGS'])
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

# to run migration:
# $ python app.py db init nb:only 1st time we make a migration
# update our models.py
# $ python app.py db migrate
# $ python app.py db upgrade

# to update heroku, push migrations folder then
# heroku run python manage.py db upgrade
