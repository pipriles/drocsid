
def test_index_redirect(client):

    resp = client.get('/')
    assert resp.status_code == 302 # Should redirect user to login

def test_get_messages(redis, client, client1):
    return

    client1.send({ 'type': 'message', 'message': 'Hello' }, json=True, namespace='/chat')
    client1.send({ 'type': 'message', 'message': 'How are you?' }, json=True, namespace='/chat')

    resp = client.get('/messages')
    msgs = resp.json

    assert len(msgs) == 2

    assert 'id' in msgs[0]
    assert msgs[0]['message'] == 'How are you?'

    assert 'id' in msgs[1]
    assert msgs[1]['message'] == 'Hello'

