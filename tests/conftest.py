import backend
import bot

import pytest
import os

from  werkzeug.security import check_password_hash, generate_password_hash

@pytest.fixture
def redis():
    redis = backend.init_redis()
    redis.flushall()
    yield redis

@pytest.fixture(scope='session')
def _create_app():
    yield backend.create_app()

@pytest.fixture(scope='session')
def app(_create_app):

    app, _ = _create_app
    app.secret_key = os.urandom(24)

    with app.app_context():
        app.config['TESTING'] = True
        yield app

@pytest.fixture(scope='session')
def socketio(_create_app):

    _, socketio = _create_app
    yield socketio

@pytest.fixture(scope='session')
def socketio_client(app, socketio):

    yield socketio.test_client(app)

@pytest.fixture
def client(app):

    with app.test_client() as client:
        yield client

@pytest.fixture
def client1(app, socketio, redis):

    username = os.urandom(4).hex()
    password = os.urandom(4).hex()

    redis.hset('users', username, generate_password_hash(password))

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['username'] = username
        yield socketio.test_client(app, namespace='/chat', flask_test_client=client)

@pytest.fixture
def client2(app, socketio, redis):

    username = os.urandom(4).hex()
    password = os.urandom(4).hex()

    redis.hset('users', username, generate_password_hash(password))

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['username'] = username
        yield socketio.test_client(app, namespace='/chat', flask_test_client=client)

