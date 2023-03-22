import re

from bson import ObjectId
from flask import Flask, render_template, jsonify, redirect, url_for, render_template_string
from flask_restful import Resource, Api
from flask_socketio import SocketIO, send
from flask import request
from accounts import accounts
from accounts import sqlDB
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from cryptography.fernet import Fernet

app = Flask("Chat")
loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = 'login'
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")

key = Fernet.generate_key()
fernet = Fernet(key)


@loginManager.user_loader
def loadUser(userID):
    return sqlDB.customers.find({'_id': ObjectId(userID)})


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
    sqlDB.switchActive(email, bool(result))
    ids = sqlDB.getUserID(email)
    idsEncr = fernet.encrypt(str(ids).encode())

    if result:
        return jsonify({'redirect': url_for('index1', ids=idsEncr)})
    else:
        return jsonify({'redirect': url_for('index')})


def check(email):
    regex = '^[a-zA-Z0-9]{3,}[-]?\@[a-zA-Z0-9]{3,}[-]?\.[a-zA-Z]{2,}$'
    if re.search(regex, email):
        return True
    else:
        return False


@app.route('/api/register', methods=['POST', 'GET'])
def register():
    data = request.json

    name = data['name']
    email = data['email']
    checks = check(email)
    age = data['age']
    amount = data['amount']
    password = data['password']
    if checks:
        accounts.Account(name, age, email, password, amount)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})


@app.route('/login')
def loginPage():
    return render_template("login.html")


@app.route('/form')
def form():
    return render_template("form.html")


@app.route('/<ids>')
def index1(ids):
    ids2 = fernet.decrypt(ids)
    ids2 = ids2.decode()
    ids2 = ObjectId(ids2)
    name = sqlDB.getUserName2(ids2)
    return render_template("index.html", name=name)


@app.route('/')
def index():
    return render_template("index.html", name="Guest")


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host="localhost", port=5000)
