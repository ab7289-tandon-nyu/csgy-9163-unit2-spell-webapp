from app import app as _app


def test_config(temp_dir, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:////{temp_dir}")
    assert not _app.create_app().testing


def test_test_config(temp_dir, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:////{temp_dir}")
    assert _app.create_app({"TESTING": True}).testing
