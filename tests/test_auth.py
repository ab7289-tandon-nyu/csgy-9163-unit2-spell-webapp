import pytest
from flask import g, session
from spellr.db import get_db


def test_register(client, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post(
        "/auth/register", data={"uname": "a", "pword": "a", "2fa": "1"}
    )
    assert "http://localhost/auth/login" == response.headers["Location"]

    with app.app_context():
        assert (
            get_db().execute("select * from user where username = 'a'",).fetchone()
            is not None
        )


@pytest.mark.parametrize(
    ("username", "password", "two_factor", "message"),
    (
        ("", "", "", b"Failure, Username is required"),
        ("a", "", "", b"Failure, Password is required."),
        ("test", "test", "1112223333", b"already registered"),
        ("a", "a", "", b"Failure, Two Factor Auth device is required."),
    ),
)
def test_register_validate_input(client, username, password, two_factor, message):
    response = client.post(
        "/auth/register", data={"uname": username, "pword": password, "2fa": two_factor}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get("/auth/login").status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "http://localhost/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test"


@pytest.mark.parametrize(
    ("username", "password", "two_factor", "message"),
    (
        ("a", "test", "1112223333", b"Incorrect username."),
        ("test", "a", "1112223333", b"Incorrect password."),
        ("test", "test", "1", b"Two Factor Device failure."),
    ),
)
def test_login_validate_input(auth, username, password, two_factor, message):
    response = auth.login(username, password, two_factor)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
