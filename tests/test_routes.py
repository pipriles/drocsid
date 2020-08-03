
def test_index_route(client):

    resp = client.get('/')
    assert resp.status_code == 200
    print(resp.data)

def test_get_messages(redis, client, client1):

    client1.send({ 'type': 'message', 'message': 'Hello' }, json=True)
    client1.send({ 'type': 'message', 'message': 'How are you?' }, json=True)

    recv = client1.get_received()

    resp = client.get('/messages')
    msgs = resp.json

    assert len(msgs) == 2

    assert 'id' in msgs[0]
    assert msgs[0]['message'] == 'How are you?'

    assert 'id' in msgs[1]
    assert msgs[1]['message'] == 'Hello'

