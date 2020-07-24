import os

from flask import Flask
from flask_principal import Principal

# from datetime import timedelta
# from app.extensions import db, csrf, login_manager, talisman
from app.extensions import db, csrf, login_manager
from app.models import User, Role


def create_app(test_config=None):
    #  create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        # DATABASE=os.path.join(app.instance_path, "spellr.sqlite",
        SQLALCHEMY_DATABASE_URI=os.getenv(
            "DATABASE_URL", "sqlite:////tmp/spellr.sqlite"
        ),
        # turned off for performance
        SQLALCHEMY_ECHO=False,
        # turned off for performance
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        # set to a short time for demonstration purposes
        # PERMANENT_SESSION_LIFETIME=timedelta(minutes=2),
        # sets the SameSite cookie option to restrict how cookies are
        # sent with requests from external sites
        SESSION_COOKIE_SAMESITE="Lax",
        DEBUG=True,
        FORCE_HTTP=False,
        STRICT_TRANSPORT_SECURITY=False,
    )

    if test_config:
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
    # csp = {
    #     "default-src": "'self'",
    #     "style-src": ["'self'", "fonts.googleapis.com"],
    #     "font-src": ["'self'", "fonts.gstatic.com"],
    #     "script-src": ["'self'", "code.jquery.com"],
    #     "frame-ancestors": "'none'",
    # }
    # talisman.init_app(app, content_security_policy=csp)

    # init flask-login
    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    # init flask-principal
    Principal(app)

    # define blueprints
    from . import auth

    app.register_blueprint(auth.bp)

    from . import spell

    app.register_blueprint(spell.bp)

    from . import history

    app.register_blueprint(history.bp)

    # since we don't have a view defined for '/' and /spell_check
    # is the main point after login, define a rule to route any requests
    # to the base URI to index, which resolves to /spellr
    app.add_url_rule("/", endpoint="index")

    # since we are outside of a request context, using app.app_context()
    # allows us to use the db variable to create the database schema
    with app.app_context():
        db.create_all()

        # create default roles
        commit = False
        if Role.query.filter_by(name="user").count() == 0:
            user_role = Role(name="user")
            db.session.add(user_role)
            commit = True
        admin_role = Role.query.filter_by(name="admin").first()
        if not admin_role:
            admin_role = Role(name="admin")
            db.session.add(admin_role)
            commit = True
        if commit:
            db.session.commit()

        if User.query.filter_by(username="admin").count() == 0:
            admin_user = User(username="admin", two_factor="12345678901")
            admin_user.set_password("Administrator@1")
            # admin_user.roles.append(user_role)
            admin_user.roles.append(admin_role)

            db.session.add(admin_user)
            db.session.commit()

    return app
