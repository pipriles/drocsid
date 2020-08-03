
def test_join(client):
    
    data = { 'username': 'hellokitty', 'password': 'hellokitty' }
    resp = client.post('/join', data=data, follow_redirects=True)

    with client.session_transaction() as session:
        assert session['username'] == 'hellokitty'

def test_invalid_join(client):

    data = { 'username': 'hellokitty', 'password': 'hellokitto' }
    resp = client.post('/join', data=data, follow_redirects=True)

    with client.session_transaction() as session:
        assert 'hellokitty' not in session
