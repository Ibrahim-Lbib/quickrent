import pytest
from app import create_app
from app.extensions import db
from app.models.user import User

@pytest.fixture
def app():
    app = create_app("test")
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def auth_client(client, app):
    """A client with a registered and logged-in user."""
    with app.app_context():
        user = User(full_name="Test User", email="test@example.com", phone="0700000000")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        
    client.post('/login', data={'email': 'test@example.com', 'password': 'password123'}, follow_redirects=True)
    return client
