from flask import Flask
from flask_socketio import SocketIO

from config import Config
from packet import Packet

app = Flask(__name__, static_url_path="", static_folder="static")
app.config.from_object(Config())
socketio = SocketIO(app)


@socketio.on("data")
def process(data):
    packet = Packet.parse(data)
    packet.handle()
