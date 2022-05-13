"""This test the homepage"""
from app import db
from app.db.models import User, Transactions

def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_auth_pages(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200

def test_login(application, client):
    """Test that a user login functionality works"""
    with application.app_context():
        #Add user to be able to test login
        user = User('test@test.com', 'testtest')
        db.session.add(user)
        db.session.commit()

        res = client.post('/login', data=dict(email="test@test.com", password='testtest'), follow_redirects=True)
        assert res.status_code == 200
        assert b"Welcome" in res.data

        #Test that the user can navigate to the dashboard and that it displays the user
        dres = client.get("/dashboard", follow_redirects=True)
        assert b"test" in dres.data

        db.session.delete(user)


def test_registration(client):
    """Test if a user logs in that it redirects to login page"""
    with client:
        res = client.post('/register', data=dict(email="test@test.com", password='testtest'), follow_redirects=True)
        print(res.data)
        assert res.status_code == 200
        assert b'href="/login"' in res.data


def test_dashboard_access(client):
    """Test dashboard access"""
    res = client.get("/dashboard")
    assert res.status_code == 302



def test_authenticated_user(client):
    """Test user authentication"""
    user = User("test@test.com", "testtest")
    assert user.is_authenticated() == True