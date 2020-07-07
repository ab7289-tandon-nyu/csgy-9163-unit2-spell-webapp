import os

from flask import Flask
from datetime import timedelta
from spellr.extensions import db, csrf, login_manager


def create_app(test_config=None):
    #  create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        # DATABASE=os.path.join(app.instance_path, "spellr.sqlite",
        SQLALCHEMY_DATABASE_URI="sqlite:////tmp/spellr.sqlite",
        SQLALCHEMY_ECHO=False,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=2),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # include db
    db.init_app(app)

    # init global CSRF protection
    csrf.init_app(app)

    # init flask-login
    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    # define blueprints
    from . import auth

    app.register_blueprint(auth.bp)

    from . import spell

    app.register_blueprint(spell.bp)

    app.add_url_rule("/", endpoint="index")

    with app.app_context():
        db.create_all()

    return app
