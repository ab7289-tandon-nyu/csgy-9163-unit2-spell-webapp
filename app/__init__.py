import os

from flask import Flask
from datetime import timedelta
from app.extensions import db, csrf, login_manager, talisman


def create_app(test_config=None):
    #  create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        # DATABASE=os.path.join(app.instance_path, "spellr.sqlite",
        SQLALCHEMY_DATABASE_URI="sqlite:////tmp/spellr.sqlite",
        # turned off for performance
        SQLALCHEMY_ECHO=False,
        # turned off for performance
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # set to a short time for demonstration purposes
        PERMANENT_SESSION_LIFETIME=timedelta(minutes=2),
        # sets the SameSite cookie option to restrict how cookies are
        # sent with requests from external sites
        SESSION_COOKIE_SAMESITE="Lax",
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

    # init xss protection
    csp = {
        "default-src": "'self'",
        "style-src": ["'self'", "fonts.googleapis.com"],
        "font-src": ["'self'", "fonts.gstatic.com"],
        "script-src": ["'self'", "code.jquery.com"],
        "frame-ancestors": "'none'",
    }
    talisman.init_app(app, content_security_policy=csp)

    # init flask-login
    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    # define blueprints
    from . import auth

    app.register_blueprint(auth.bp)

    from . import spell

    app.register_blueprint(spell.bp)

    # since we don't have a view defined for '/' and /spell_check
    # is the main point after login, define a rule to route any requests
    # to the base URI to index, which resolves to /spellr
    app.add_url_rule("/", endpoint="index")

    # since we are outside of a request context, using app.app_context()
    # allows us to use the db variable to create the database schema
    with app.app_context():
        db.create_all()

    return app
