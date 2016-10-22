from flask import Flask
from flask_socketio import SocketIO

import views
from config import Config

app = Flask(__name__, static_url_path="", static_folder="static")
app.config.from_object(Config())
socketio = SocketIO(app)

app.register_blueprint(views.blueprint)
