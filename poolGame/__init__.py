from flask import Flask
from flask_socketio import SocketIO, emit
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
from poolGame import routes

