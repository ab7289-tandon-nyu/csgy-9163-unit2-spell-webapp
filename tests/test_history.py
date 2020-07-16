import pytest


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
    ),
)
def test_history_inputs(auth, client, query, message):
    auth.login()
    response = client.post("/history", data={"userquery": query})

    assert response.status_code == 200
    assert message in response.data
