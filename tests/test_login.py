
def test_login(client):
    
    data = { 'username': 'hellokitty' }
    resp = client.post('/login', json=data)
    data = resp.json

    print(data)

    assert data['id'] == 'hellokitty'
