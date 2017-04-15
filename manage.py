import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app


app.config.from_object(os.environ['APP_SETTINGS'])

manager = Manager(app)


if __name__ == '__main__':
    manager.run()
