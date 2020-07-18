import pytest

from spellr.models import User, Question
from spellr.extensions import db


def test_history(client, auth):
    auth.login()

    assert client.get("/history").status_code == 200


@pytest.mark.parametrize(
    ("query", "message"),
    (
        ("a", b"Field must be between 3 and 25 characters long"),
        (
            "asdfasdfasdfasdfasdfasdfasdf",
            b"Field must be between 3 and 25 characters long",
        ),
        ("test", b"user_id: test"),
        ("test2", b"Unable to find a registered user for user_id"),
    ),
)
def test_history_inputs(auth, client, query, message):
    auth.login()
    response = client.post("/history", data={"userquery": query})

    assert response.status_code == 200
    assert message in response.data


def test_history_item_not_found(auth, client):
    auth.login()
    response = client.get("/history/query999")

    assert response.status_code == 200
    assert b"No Item Found" in response.data


def test_history_item_found(auth, client):

    test_user = User.query.filter_by(username="test").one()

    q = Question(text="some text", result="no errors")
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


def test_login_history_auth(auth, client):
    assert client.get("/login_history").status_code == 302
    auth.login()
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
        ("test", b"Login ID"),
    ),
)
def test_login_history_results(auth, client, query, message):
    auth.login()
    response = client.post("/login_history", data={"userid": query})

    assert response.status_code == 200
    assert message in response.data
