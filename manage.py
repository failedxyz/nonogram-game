from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import app, socketio
from models import db

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)


@manager.command
def runserver():
    socketio.run(app, host="0.0.0.0", port=4000, use_reloader=True)


if __name__ == "__main__":
    manager.run()
