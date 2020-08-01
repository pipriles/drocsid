import backend
import pytest
import os

@pytest.fixture(scope='session')
def rd():
    return backend.init_redis()

@pytest.fixture(scope='session')
def app(rd):

    app, socketio = backend.create_app()
    app.secret_key = os.urandom(24)

    with app.app_context():
        app.config['TESTING'] = True
        yield app

@pytest.fixture
def client(app):

    with app.test_client() as client:
        yield client

