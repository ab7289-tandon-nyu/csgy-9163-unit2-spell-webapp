import os
import tempfile

import pytest

# from app import create_app
# from app import app as _app
from app import create_app
from app.extensions import db as _db
from app.models import User, Role


@pytest.fixture
def app():
    # create a temporary file path to store our db in
    # this helps to keep us from cluttering up our directories after
    # multiple test runs
    db_fd, db_path = tempfile.mkstemp()

    # define the app with a test configuration
    app = create_app(
        {
            # setting debug to true so unittests will run in travis
            "DEBUG": True,
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:////{db_path}",
            # disable CSRF when testing so we can test form URI submission
            "WTF_CSRF_ENABLED": False,
            "WTF_CSRF_METHODS": [],
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )  # noqa: E231

    with app.app_context():
        # do db setup prior to test runs
        _db.create_all()
        # create a user to test with
        user = User(username="test", two_factor="1231231234",)
        user.set_password("test")
        admin_user = User(username="test_admin", two_factor="1231231234")
        admin_user.set_password("test_admin")
        admin_role = Role.query.filter_by(name="admin").one()
        admin_user.roles.append(admin_role)

        _db.session.add(user)
        _db.session.add(admin_user)
        _db.session.add(admin_role)
        _db.session.commit()
        # pass the app to the fixture so it can be utilized in each test
        yield app
        # after each test, clear the db session and drop the database
        _db.session.remove()
        _db.drop_all()

    # finally destroy the temp directories we created
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    # returns a client object that we can do HTTP request with
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    """ convenience class to simplify loggin in and out in tests """

    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test", two_factor="1231231234"):
        return self._client.post(
            "/login",
            data={"username": username, "password": password, "two_factor": two_factor},
        )

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    """ fixture to provide the AuthActions class to tests """
    return AuthActions(client)


@pytest.fixture
def temp_dir():
    db_fd, db_path = tempfile.mkstemp()

    yield db_path

    # finally destroy the temp directories we created
    os.close(db_fd)
    os.unlink(db_path)
