from flask import Flask, render_template, jsonify
from flask_restful import Resource, Api
from flask_socketio import SocketIO, send
from flask import request
from accounts import accounts

app = Flask("LotteryAPI")
socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('message')
def handleMessage(message):
    print("Received message: " + message)
    if message != "User connected!":
        send(message, broadcast=True)


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json

    email = data['email']
    password = data['password']

    print(email + " " + password)
    return jsonify({'success': 100})


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json

    name = data['name']
    email = data['email']
    age = data['age']
    amount = data['amount']
    password = data['password']

    acc = accounts.Account(name, age, email, password, amount)
    print(acc.isActive())
    # Return a response to the client
    return jsonify({'success': str(acc.isActive())})


@app.route('/login')
def loginPage():
    return render_template("login.html")


@app.route('/form')
def form():
    return render_template("form.html")


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, allow_unsafe_werkzeug=True, host="localhost", port=5000)
