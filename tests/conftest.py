import backend
import pytest
import os

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
def client1(app, socketio):

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['username'] = os.urandom(4).hex()
        yield socketio.test_client(app, flask_test_client=client)

@pytest.fixture
def client2(app, socketio):

    with app.test_client() as client:
        with client.session_transaction() as session:
            session['username'] = os.urandom(4).hex()
        yield socketio.test_client(app, flask_test_client=client)

