import pytest


def test_index(client, auth):
    response = client.get("/spell_check")
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get("/spell_check")
    assert b"Log Out" in response.data
    assert b"Spellr" in response.data
    assert b"test_user" in response.data
