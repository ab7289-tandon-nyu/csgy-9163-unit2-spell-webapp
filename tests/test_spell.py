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


def test_spell_valid(client, auth):
    auth.login()
    assert client.get("/spell_check").status_code == 200
    response = client.post("/spell_check", data={"inputtext": "This is a test."})

    assert b"All words are correctly spelled" in response.data


def test_spell_invalid(client, auth):
    auth.login()
    assert client.get("/spell_check").status_code == 200
    response = client.post("/spell_check", data={"inputtext": "This is a tset."})

    assert b"words are misspelled" in response.data
