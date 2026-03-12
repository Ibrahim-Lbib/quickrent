def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"QuickRent" in response.data

def test_register(client, app):
    response = client.post('/register', data={
        'full_name': 'New User',
        'email': 'new@example.com',
        'phone': '0701111111',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Account created successfully" in response.data

def test_login(client, auth_client):
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b"Test User" in response.data

def test_logout(auth_client):
    response = auth_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"QuickRent" in response.data
