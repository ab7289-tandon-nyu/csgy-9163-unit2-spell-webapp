# import pytest


def test_index(client, auth):
    response = client.get("/spell_check")
    print(f"result1: {response}")
    assert response.status_code == 302
    assert "http://localhost/auth/login" == response.headers["Location"]

    auth.login()
    response = client.get("/spell_check")
    assert b"Log Out" in response.data
    assert b"Spellr" in response.data
    assert b"test" in response.data
