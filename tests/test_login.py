
def test_login(client):
    
    data = { 'username': 'hellokitty' }
    resp = client.post('/login', json=data)
    data = resp.json

    with client.session_transaction() as session:
        assert session['username'] == 'hellokitty'

    assert data['id'] == 'hellokitty'
