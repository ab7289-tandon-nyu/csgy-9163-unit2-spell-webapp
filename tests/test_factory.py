from spellr import create_app


def test_config(temp_dir, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:////{temp_dir}")
    assert not create_app().testing


def test_test_config(temp_dir, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:////{temp_dir}")
    assert create_app({"TESTING": True}).testing
