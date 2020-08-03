#!/usr/bin/env python3

import redis
import os
import json
import uuid

from flask import Flask, request, session, jsonify, render_template
from flask_socketio import SocketIO, emit, send

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB   = 0
REDIS_CHANNEL = 'chat'

def init_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def fetch_messages(r):
    chat = r.lrange('chat', 0, 50)
    return [ json.loads(msg.decode('utf8')) for msg in chat ]

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24).hex()

    rd = init_redis()
    socketio = SocketIO(app)

    # def on_publish(message):
    #     data = message['data']
    #     post = json.loads(data.decode('utf8'))
    #     print('[REDIS]', post)
    #     socketio.send(post, json=True)

    # p = rd.pubsub()
    # p.subscribe(**{REDIS_CHANNEL: on_publish})
    # thread = p.run_in_thread(sleep_time=0.001)

    # def teardown_redis(exception):
    #     print('STOP!')
    #     thread.stop()

    # app.teardown_appcontext(teardown_redis)

    @app.route('/')
    @app.route('/index')
    def index():
        # Show app homepage
        # if not session redirect to login page
        messages = fetch_messages(rd)
        messages = reversed(messages)
        return render_template('index.html', messages=messages)

    @app.route('/login', methods=['POST'])
    def login():
        # Validate user login against redis
        username = request.json['username']
        session['username'] = username
        return { 'id': username }

    @app.route('/register', methods=['POST'])
    def register():
        # Store user on redis database
        # encrypt password using werkzeug
        pass

    @app.route('/messages')
    def messages():
        # Fetch messages from redis 
        chat = rd.lrange('chat', 0, 50)
        decoded = [ json.loads(msg.decode('utf8')) for msg in chat ]

        # reverse order and filter commands?
        return jsonify(decoded)

    @socketio.on('connect')
    def on_connect():
        # Verify user is authenticated
        # so he can not listen the chat
        print('Someone connected...')

    @socketio.on('json')
    def on_message(message):

        # Verify username (is valid and logged)
        # Verify type of message (command, message)
        # Validate keys are present
        # type and username
        # sanitize messages
        # do not store on redis if message is a command

        # Verify message username matches session username
        # if 'username' not in session \
        # or session['username'] == message.get('username'):
        #     print('Username does not match!')
        #     return


        if message['type'] == 'message':
            message['id'] = str(uuid.uuid4())
            rd.lpush('chat', json.dumps(message))

        elif message['type'] != 'command':
            print('Unsupported type message', message['type'])
            return

        print(message)
        socketio.emit('message', message)

    return app, socketio

