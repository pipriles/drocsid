#!/usr/bin/env python3

import redis
import os
import json
import uuid
import re

from flask import Flask, request, session, jsonify, render_template, redirect, url_for, escape, current_app
from flask_socketio import SocketIO, emit, send, disconnect, join_room, leave_room
from werkzeug.security import generate_password_hash, check_password_hash

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = 6379
REDIS_DB   = 0
REDIS_CHANNEL = 'chat'

GLOBAL_CHAT = 'global'

def init_redis():
    return redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def fetch_messages(r):
    room = current_room(r, GLOBAL_CHAT)
    key = 'room:' + room
    chat = r.lrange(key, 0, 49)
    return [ json.loads(msg.decode('utf8')) for msg in chat ]

def current_room(rd, default=None):

    user = session.get('username')
    key  = 'user:{}'.format(user)

    room = rd.get(key)
    return default if room is None else room.decode('utf8')

def set_current_room(rd, room):

    user = session.get('username')
    key  = 'user:{}'.format(user)

    return rd.set(key, room)

def has_bot_token():

    auth = request.headers.get('Authorization')
    if auth is None: return False

    match = re.match('BotToken (\w+)', auth)
    token = match.group(1) if match else None

    return current_app.config['BOT_TOKEN'] == token

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24).hex()
    app.config['BOT_TOKEN']  = os.environ.get('BOT_TOKEN', '38f51666d5dffdb15fc06d1ef4dfd0c1ccd1a8daed2b3312')

    rd = init_redis()
    socketio = SocketIO(app)

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

        room = current_room(rd, GLOBAL_CHAT)

        messages = fetch_messages(rd)
        messages = reversed(messages)
        
        return render_template('index.html', messages=messages, room=room)

    @app.route('/exit')
    def exit_chat():
        session.clear()
        return redirect(url_for('index'))

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

    @socketio.on('connect')
    def on_connect():

        print('Client connected.', session.get('username'))

        if  not has_bot_token() \
        and not is_authenticated():

            print('Client disconnected.')
            disconnect()

    @socketio.on('connect', namespace='/bot')
    def on_bot_connect():
        # Verify user is authenticated
        # so he can not listen the chat
        print('Bot connected.')

        if not has_bot_token():
            print('Bot disconnected.')
            disconnect()
    
    @socketio.on('json', namespace='/bot')
    def on_bot_message(message):

        message['id'] = str(uuid.uuid4())
        message['username'] = 'bot'

        # Sanitize messages (We don't trust the user)
        message['message'] = escape(message['message']) 

        if message['type'] == 'message':
            # Store on redis if it is only a message
            rd.lpush('chat', json.dumps(message))

        socketio.emit('message', message, namespace='/chat')

    @socketio.on('connect', namespace='/chat')
    def on_user_connect():

        # Verify user is authenticated
        # so he can not listen the chat

        # Join to global room initally

        if not is_authenticated():
            disconnect()
        else:
            user = session.get('username')
            room = current_room(rd, GLOBAL_CHAT)

            print('Someone has joined the chat...', user)
            join_room(room)

    @socketio.on('json', namespace='/chat')
    def on_user_message(message):

        # Verify username (is valid and logged)
        if not is_authenticated():
            disconnect()
            return

        message['id'] = str(uuid.uuid4())
        message['username'] = session.get('username')

        # Sanitize messages (We don't trust the user)
        message['message'] = escape(message['message']) 

        room = current_room(rd, GLOBAL_CHAT)
        print('Message on room:', room)

        if message['type'] == 'message':
            # Store on redis if it is only a message
            key = 'room:' + room
            rd.lpush(key, json.dumps(message))

        elif message['type'] == 'command':
            # Emit message to bot namespace
            socketio.emit('message', message, namespace='/bot')

        emit('message', message, namespace='/chat', room=room)

    @socketio.on('join', namespace='/chat')
    def on_room_join(data):

        user = session['username']

        prev = current_room(rd, GLOBAL_CHAT)
        print('Previous room', prev)

        room = data.get('room', GLOBAL_CHAT)
        set_current_room(rd, room)

        leave_room(prev)
        join_room(room)

        message = '{} has joined the chat'.format(user)
        payload = { 'message': message }

        emit('status', payload, namespace='/chat', room=room)
        print(user, 'has joined room:', room)

    return app, socketio

