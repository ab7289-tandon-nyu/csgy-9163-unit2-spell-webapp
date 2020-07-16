import pytest

from spellr.models import User, Role, Question
from spellr.extensions import db


@pytest.mark.usefixtures("app")
class TestUser:
    def test_user(self):
        new_user = User(username="new_user", two_factor="1231231234")

        assert new_user.username == "new_user"
        assert new_user.two_factor == "1231231234"
        assert new_user.password is None

        new_user.set_password("password")

        assert new_user.password != "password"
        assert new_user.check_password("password") is True

    def test_save(self):
        new_user = User(username="new_user", two_factor="1231231234")
        new_user.set_password("password")

        db.session.add(new_user)
        db.session.commit()

        found_user = User.query.get(new_user.id)

        assert found_user.username == "new_user"
        assert found_user.two_factor == "1231231234"
        assert found_user.check_password("password") is True
        assert found_user == new_user

    def test_user_roles(self):
        new_user = User(username="new_user", two_factor="1231231234")
        new_user.set_password("password")

        db.session.add(new_user)
        db.session.commit()

        user_role = Role.query.filter_by(name="user").first()
        assert user_role in new_user.roles


@pytest.mark.usefixtures("app")
class TestRoles:
    def test_role(self):
        new_role = Role(name="test_role")

        assert new_role.name == "test_role"

    def test_save_role(self):
        new_role = Role(name="test_role")

        db.session.add(new_role)
        db.session.commit()

        found_role = Role.query.filter_by(name="test_role").first()

        assert found_role.name == "test_role"
        assert found_role == new_role


@pytest.mark.usefixtures("app")
class TestQuestions:
    def test_question(self):
        test_user = User.query.filter_by(username="test").one()
        q = Question(text="some text", result="no errors")
        test_user.questions.append(q)

        db.session.add(q)
        db.session.commit()

        q_list = Question.query.filter_by(user_id=test_user.id).one()

        assert q_list == q

    def test_question_backref(self):
        test_user = User.query.filter_by(username="test").one()
        q = Question(text="some text", result="no errors")
        test_user.questions.append(q)

        db.session.add(q)
        db.session.commit()

        q_user = User.query.get(q.user.id)

        assert q_user == test_user
