import pytest

from app.models import User, Question
from app.extensions import db


def create_question(text="some text", result="no errors"):
    return Question(text=text, result=result)


def test_history(client, auth):
    assert client.get("/history").status_code == 302
    auth.login()
    assert client.get("/history").status_code == 200


def test_history_user_access(client, auth):
    auth.login()
    response = client.get("/history")
    assert response.status_code == 200
    assert b"<form" not in response.data


@pytest.mark.parametrize(
    ("query", "status_code", "message"),
    (
        ("a", "200", b"Field must be between 3 and 25 characters long"),
        (
            "asdfasdfasdfasdfasdfasdfasdf",
            "200",
            b"Field must be between 3 and 25 characters long",
        ),
        ("test", "200", b"user_id: test"),
        ("test2", "200", b"Unable to find a registered user for user_id"),
    ),
)
def test_history_inputs(auth, client, query, status_code, message):
    auth.login(username="test_admin", password="test_admin")
    response = client.post("/history", data={"userquery": query})

    assert response.status_code == int(status_code)
    assert message in response.data


def test_history_admin_access(auth, client):

    auth.login(username="test_admin", password="test_admin")
    response = client.post("/history", data={"userquery": "test"})

    assert response.status_code == 200
    assert b"<form" in response.data


def test_history_item_not_found(auth, client):
    auth.login()
    response = client.get("/history/query999")

    assert response.status_code == 200
    assert b"No Item Found" in response.data


def test_history_item_found(auth, client):

    test_user = User.query.filter_by(username="test").one()

    q = create_question()
    test_user.questions.append(q)

    db.session.add(q)
    db.session.commit()

    auth.login()
    response = client.get(f"/history/query{q.id}")

    assert response.status_code == 200
    assert b"some text" in response.data
    assert b"no errors" in response.data
    assert b"test" in response.data
    assert f"Query{q.id}" in str(response.data)


def test_history_item_unauthenticated(auth, client):
    test_admin = User.query.filter_by(username="test_admin").one()
    q = create_question()
    test_admin.questions.append(q)

    db.session.add(q)
    db.session.commit()

    auth.login()
    assert client.get(f"/history/query{q.id}").status_code == 403


def test_login_history_auth(auth, client):
    assert client.get("/login_history").status_code == 302
    auth.login()
    assert client.get("/login_history").status_code == 403
    auth.login(username="test_admin", password="test_admin")
    assert client.get("/login_history").status_code == 200


@pytest.mark.parametrize(
    ("query", "message"),
    (
        ("a", b"Field must be between 3 and 25 characters long"),
        (
            "asdfasdfasdfasdfasdfasdfasdf",
            b"Field must be between 3 and 25 characters long",
        ),
        ("test2", b"Unable to find a registered user for user_id"),
        ("test_admin", b"Login ID"),
    ),
)
def test_login_history_results(auth, client, query, message):
    auth.login(username="test_admin", password="test_admin")
    response = client.post("/login_history", data={"userid": query})

    assert response.status_code == 200
    assert message in response.data
