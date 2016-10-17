from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

from app import app
from models import db

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

server_command = Server(host="0.0.0.0", port=5000, use_debugger=True, use_reloader=True)
manager.add_command("runserver", server_command)

if __name__ == "__main__":
    manager.run()
