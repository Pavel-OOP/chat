from flask import Flask, render_template, jsonify, redirect, url_for
from flask_restful import Resource, Api
from flask_socketio import SocketIO, send
from flask import request
from accounts import accounts
from accounts import sqlDB
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

app = Flask("Chat")
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login'
socketio = SocketIO(app, cors_allowed_origins="*")


@loginManager.user_loader
def loadUser(userID):
    return sqlDB.customers.find({'_id': userID})


@socketio.on('message')
def handleMessage(message):
    print("Received message: " + message)
    if message != "User connected!":
        send(message, broadcast=True)


@app.route('/api/login', methods=['GET', 'POST'])
def login():
    data = request.json

    email = data['email']
    password = data['password']
    result = sqlDB.login(email, password)
    if result:  # todo
        return redirect(url_for('index', email=email))

    return jsonify({'success': str(result)})


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json

    name = data['name']
    email = data['email']
    age = data['age']
    amount = data['amount']
    password = data['password']

    result = accounts.Account(name, age, email, password, amount)
    print(result.isActive())
    # Return a response to the client
    return jsonify({'success': str(result.isActive())})


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
