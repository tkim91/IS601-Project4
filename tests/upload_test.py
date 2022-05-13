from flask import url_for


def test_csv_upload_access_denied(client):
    with client:
        """This tests for checking if access to songs upload page is denied without login"""
        response = client.get("/transactions/upload")
        assert response.status_code == 302
        response_csv = client.get("/transactions/upload", follow_redirects=True)
        assert response_csv.request.path == url_for('auth.login')
        assert response_csv.status_code == 200