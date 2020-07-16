from spellr.models import Question, User


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

def test_question_save(client, auth):
    auth.login()
    assert client.get("/spell_check").status_code == 200
    client.post("/spell_check", data={"inputtext": "This is a test."})

    test_user = User.query.filter_by(username="test").one()
    q_list = test_user.questions
    assert len(q_list) == 1
    assert  "This is a test." in q_list[0].text
    assert "All words are correctly spelled" in q_list[0].result 


