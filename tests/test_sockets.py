import time

def test_socket(socketio_client, redis, client1):

    client1.send({ 'type': 'message', 'message': 'test_socket' }, json=True, namespace='/chat')
    recv = client1.get_received('/chat')

    assert recv[0]['args']['type'] == 'message'
    assert recv[0]['args']['message'] == 'test_socket'

def test_multiple_clients(app, socketio, redis, client1, client2):

    client1.send({ 'type': 'message', 'message': 'from_client_1' }, json=True, namespace='/chat')

    start = time.time()
    timeout = 2

    while True: 
        # Wait until received
        recv = client2.get_received('/chat')
        if recv: break
        if time.time() - start > timeout:
            raise TimeoutError('No message received')
        time.sleep(0.01)

    assert recv[0]['args']['type']    == 'message'
    assert recv[0]['args']['message'] == 'from_client_1'

def test_join_room(app, socketio, client1, client2):

    client1.emit('join', { 'room': 'room1' }, namespace='/chat')
    client1.send({ 'type': 'message', 'message': 'foobar' }     , json=True, namespace='/chat')

    # Wait until received
    recv = client2.get_received('/chat')

    assert not recv

    client2.emit('join', { 'room': 'room1' }, namespace='/chat')
    client1.send({ 'type': 'message', 'message': 'foobar' }, json=True, namespace='/chat')

    recv = client2.get_received('/chat')

    assert len(recv) == 2
    assert recv[1]['args']['message'] == 'foobar'

