import os

from flask import Flask
from flask_socketio import SocketIO, emit

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24).hex()
    socketio = SocketIO(app)

    @app.route('/')
    def index():
        # Show app homepage
        pass

    @app.route('/login', methods=['POST'])
    def login():
        # Validate user login against redis
        pass

    @app.route('/register', methods=['POST'])
    def login():
        # Register user
        pass

    @app.route('/messages')
    def messages():
        # Fetch messages from redis 
        pass

    @socketio.on('message')
    def on_message(message):
        # Publish message in redis channel
        # Add message to list on redis
        pass

    return socketio

