from flask import url_for


def test_register(client):
    """Tests for registration SUCCESS"""
    with client:
        response = client.post("/register", data={
            "email": "test@test.com",
            "password": "testtest",
            "confirm": "testtest"
        }, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == url_for('auth.login')


def test_login(client):
    """Tests for login SUCCESS"""
    with client:
        response = client.post("/register", data={
            "email": "test@test.com",
            "password": "testtest",
            "confirm": "testtest"
        }, follow_redirects=True)

        assert response.status_code == 200
        assert response.request.path == url_for('auth.login')

        login_response = client.post("/login", data={
            "email": "test@test.com",
            "password": "testtest",
        }, follow_redirects=True)
        assert login_response.request.path == url_for('auth.dashboard')
        assert login_response.status_code == 200


def test_dashboard_access_success(client):
    """Tests for access to the dashboard after login SUCCESS"""
    with client:
        login_response = client.post("/login", data={
            "email": "test@test.com",
            "password": "testtest",
        }, follow_redirects=True)
        assert login_response.request.path == url_for('auth.dashboard')
        assert login_response.status_code == 200


def test_dashboard_access_denied(client):
    """Tests for accessing to the dashboard after login is UNSUCCESSFUL"""
    with client:
        response = client.post("/register", data={
            "email": "test@test.com",
            "password": "testtest",
            "confirm": "testtest"
        }, follow_redirects=True)

        assert response.status_code == 200
        assert response.request.path == url_for('auth.login')

        login_response = client.post("/login", data={
            "email": "test@test.com",
            "password": "testtest",
        }, follow_redirects=True)
        assert login_response.request.path == url_for('auth.login')
        assert login_response.status_code == 200