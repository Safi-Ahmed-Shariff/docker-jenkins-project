import pytest
from app import app, db, User
from flask import url_for

@pytest.fixture
def client():
    # Set up the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory test database
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables for testing
            # Add test data
            test_user = User(username="testuser", password="password123")
            db.session.add(test_user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after tests

def test_register_new_user(client):
    new_user_data = {'username': 'newuser', 'password': 'newpassword'}
    response = client.post('/register', data=new_user_data)
    assert response.status_code == 201  # Assuming 201 for successful creation
    assert response.get_json() == {"message": "User registered successfully"}

def test_duplicate_username(client):
    duplicate_user_data = {'username': 'testuser', 'password': 'password123'}
    response = client.post('/register', data=duplicate_user_data)
    assert response.status_code == 409  # Assuming 409 Conflict for duplicate entry
    assert response.get_json() == {"message": "Username already exists"}

def test_successful_login(client):
    response = client.post('/login', data={'username': 'testuser', 'password': 'password123'})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Login successful"}

def test_invalid_login(client):
    response = client.post('/login', data={'username': 'testuser', 'password': 'wrongpassword'})
    assert response.status_code == 401
    assert response.get_json() == {"message": "Invalid credentials"}

def test_missing_username(client):
    response = client.post('/login', data={'password': 'password123'})
    assert response.status_code == 400  # Assuming 400 for bad request
    assert response.get_json() == {"message": "Missing username or password"}

def test_missing_password(client):
    response = client.post('/login', data={'username': 'testuser'})
    assert response.status_code == 400  # Assuming 400 for bad request
    assert response.get_json() == {"message": "Missing username or password"}
