import os
import tempfile

import pytest
from spellr import create_app
from spellr.extensions import db as _db
from spellr.models import User

from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:////{db_path}",
            "WTF_CSRF_ENABLED": False,
            "WTF_CSRF_METHODS": [],
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )  # noqa: E231

    with app.app_context():
        _db.create_all()
        user = User(
            username="test",
            password=generate_password_hash("test"),
            two_factor="1231231234",
        )
        _db.session.add(user)
        _db.session.commit()
        yield app
        _db.session.remove()
        _db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test", two_factor="1231231234"):
        return self._client.post(
            "/auth/login",
            data={"username": username, "password": password, "two_factor": two_factor},
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
