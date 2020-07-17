import pytest
from flask import session
from datetime import datetime
from spellr.models import User, AuthHistory


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post(
        "/auth/register",
        data={"username": "aaa", "password": "aaaaaa", "two_factor": "1112223333"},
    )
    assert "/auth/login" in response.headers.get("Location")

    with app.app_context():
        assert User.query.filter_by(username="aaa").first() is not None


@pytest.mark.parametrize(
    ("username", "password", "two_factor", "message"),
    (
        ("", "", "", b"Failure, Username is required"),
        ("a", "", "", b"Failure, Password is required."),
        ("test", "test", "1112223333", b"already registered"),
        ("a", "a", "", b"Failure, Two Factor Auth device is required."),
        ("test", "test", "12", b"Failure, invalid phone number."),
        ("test", "test", "abc", b"Failure, invalid phone number."),
    ),
)
def test_register_validate_input(app, client, username, password, two_factor, message):
    response = client.post(
        "/auth/register",
        data={"username": username, "password": password, "two_factor": two_factor},
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get("/auth/login").status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "http://localhost/"

    with client:
        client.get("/")
        assert session["_user_id"] == "2"
        assert session["identity.id"] == 2

    test_user = User.query.filter_by(username="test").one()
    hist = AuthHistory.query.filter_by(user_id=test_user.id).one()
    # only login should be filled in at this point
    assert hist.login is not None
    assert hist.logout is None
    assert isinstance(hist.login, datetime)


@pytest.mark.parametrize(
    ("username", "password", "two_factor", "message"),
    (
        ("a", "test", "1231231234", b"Incorrect username or password"),
        ("test", "a", "1231231234", b"Incorrect username or password"),
        ("test", "test", "1", b"Two-factor auth device failure"),
        ("", "test", "1", b""),
    ),
)
def test_login_validate_input(auth, username, password, two_factor, message):
    response = auth.login(username, password, two_factor)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "_user_id" not in session
        # verify flask-principal session keys have been removed
        assert session.get("identity.id") is None
        assert session.get("identity.auth_type") is None
    
    test_user = User.query.filter_by(username="test").one()
    hist = AuthHistory.query.filter_by(user_id=test_user.id).one()
    assert hist.login is not None
    assert hist.logout is not None
    assert isinstance(hist.login, datetime)
    assert isinstance(hist.logout, datetime)
