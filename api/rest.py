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
api = Api(app)
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
    sqlDB.switchActive(email, bool(result))
    name = sqlDB.getUserName(email)

    return index(name, result)


@app.route('/', methods=['GET', 'POST'])
def logged():
    if request.method == 'POST':
        result = request.form
        print(result)
        return render_template("index.html", result=result)


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
def index(name="Guest", active=False):
    if not active:
        return render_template("index.html", name="Guest")
    else:
        return render_template("index.html", name=name)


if __name__ == "__main__":
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, host="localhost", port=5000)
