#!/usr/bin/env python3

import redis
import os
import json
import uuid

from flask import Flask, request, session, jsonify, render_template, redirect, url_for
from flask_socketio import SocketIO, emit, send, disconnect
from werkzeug.security import generate_password_hash, check_password_hash

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB   = 0
REDIS_CHANNEL = 'chat'

def init_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def fetch_messages(r):
    chat = r.lrange('chat', 0, 49)
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

    def is_authenticated():
        username = session.get('username')
        return username is not None and rd.hexists('users', username)

    @app.route('/')
    @app.route('/index')
    def index():
        # Show app homepage
        # if not session redirect to login page

        if not is_authenticated():
            return redirect(url_for('join'))

        messages = fetch_messages(rd)
        messages = reversed(messages)
        
        return render_template('index.html', messages=messages)

    @app.route('/join', methods=('GET', 'POST'))
    def join():

        # Store user on redis database
        # encrypt password using werkzeug

        if request.method == 'GET':
            return render_template('join.html')

        username = request.form['username']
        password = request.form['password']

        error = None

        if not username:
            error = 'Username is required'

        elif not password:
            error = 'Password is required'

        elif not rd.hexists('users', username):
            # Create user and if did not exist
            rd.hset('users', username, generate_password_hash(password))

        else:
            pwhash = rd.hget('users', username)
            pwhash = pwhash.decode('utf8')
            if not check_password_hash(pwhash, password):
                error = 'Password does not match.\nTry another username?'

        if error is None:
            session.clear()
            session['username'] = username
            return redirect(url_for('index'))

        return render_template('join.html', error=error)

    @app.route('/messages')
    def messages():
        # Fetch messages from redis 
        chat = rd.lrange('chat', 0, 49)
        decoded = [ json.loads(msg.decode('utf8')) for msg in chat ]

        # reverse order and filter commands?
        return jsonify(decoded)

    @socketio.on('connect')
    def on_connect():

        print('CONNECTED!', session.get('username'))

        if not is_authenticated():
            print('DISCONNECTED!')
            disconnect()

    @socketio.on('connect', namespace='/bot')
    def on_bot_connect():
        # Verify user is authenticated
        # so he can not listen the chat
        print('Bot connected')
        print(request.remote_addr, request.host)
        print(session)

    @socketio.on('connect', namespace='/chat')
    def on_user_connect():

        # Verify user is authenticated
        # so he can not listen the chat

        if not is_authenticated():
            disconnect()
        else:
            user = session.get('username')
            print('Someone has joined the chat...', repr(user))

    @socketio.on('json', namespace='/chat')
    def on_message(message):

        # sanitize messages

        # Verify message username matches session username
        # if 'username' not in session \
        # or session['username'] == message.get('username'):
        #     print('Username does not match!')
        #     return

        # Verify username (is valid and logged)
        if not is_authenticated():
            disconnect()
            return

        message['id'] = str(uuid.uuid4())
        message['username'] = session.get('username')

        if message['type'] == 'message':
            # Store on redis if it is only a message
            rd.lpush('chat', json.dumps(message))

        elif message['type'] == 'command':
            # Emit message to bot namespace
            socketio.emit('message', message, namespace='/bot')

        socketio.emit('message', message, namespace='/chat')

    return app, socketio

