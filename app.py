import json

from flask import Flask, session, send_file
from flask_socketio import SocketIO, emit

from channel import Channel
from config import Config
from data import clients
from packet import Packet
from util import encrypt

app = Flask(__name__, static_url_path="", static_folder="static")
app.config.from_object(Config())
socketio = SocketIO(app)

lobby = Channel("lobby", autojoin=True)


@app.route("/")
def index():
    return send_file("static/index.html")


@socketio.on("data")
def process(data):
    packet = Packet.parse(data)
    result = packet.handle()
    if result:
        header, object = result
        output = json.dumps(object)
        if header > 1:
            output = encrypt(output, packet.client.connection_key)
        emit("data", "{:0>3}{}".format(header, output))


@socketio.on("disconnect")
def disconnect():
    if "uid" in session:
        uid = session["uid"]
        if uid in clients:
            del clients[uid]
