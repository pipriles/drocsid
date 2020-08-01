#!/usr/bin/env python3

import redis
import os

from flask import Flask, request, session
from flask_socketio import SocketIO, emit

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB   = 0

def init_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24).hex()

    rd = init_redis()
    print(rd)
    rd.set('EPA', None)
    socketio = SocketIO(app)

    @app.route('/')
    def index():
        # Show app homepage
        pass

    @app.route('/login', methods=['POST'])
    def login():
        # Validate user login against redis
        username = request.json['username']
        return { 'id': username }

    @app.route('/register', methods=['POST'])
    def register():
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

    return app, socketio

