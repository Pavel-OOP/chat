from flask import Flask, render_template
from flask_restful import Resource, Api
from flask_socketio import SocketIO, send

app = Flask("LotteryAPI")
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('message')
def handleMessage(message):
    print("Received message: " + message)
    if message != "User connected!":
        send(message, broadcast=True)


@app.route('/form')
def form():
    return render_template("form.html")


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, allow_unsafe_werkzeug=True, host="localhost", port=5000)
