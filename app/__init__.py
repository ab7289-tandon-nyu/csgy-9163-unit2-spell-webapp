from importlib import import_module

from flask import Flask
from flask_principal import Principal

# from datetime import timedelta
# from app.extensions import db, csrf, login_manager, talisman
from app.extensions import db, csrf, login_manager
from app.models import User, Role


def create_app(config_object="app.settings", test_config=None):
    #  create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_object)

    if test_config:
        # load the test config if passed in
        app.config.from_mapping(test_config)

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

        # create the config object so that we can access the user values
        config_module = import_module(config_object)

        # check if admin user is defined and create user if it is defined and
        # doesn't already exist
        if (
            config_module.ADMIN_USER
            and User.query.filter_by(username=config_module.ADMIN_USER).count() == 0
        ):
            admin_user = User(
                username=config_module.ADMIN_USER, two_factor=config_module.ADMIN_TF
            )
            admin_user.set_password(config_module.ADMIN_PASS)
            # admin_user.roles.append(user_role)
            admin_user.roles.append(admin_role)

            db.session.add(admin_user)
            db.session.commit()

        # check if test user is defined and create user if it is defined and
        # doesn't already exist
        if (
            config_module.TEST_USER
            and User.query.filter_by(username=config_module.TEST_USER).count() == 0
        ):
            test_user = User(
                username=config_module.TEST_USER, two_factor=config_module.TEST_TF
            )
            test_user.set_password(config_module.TEST_PASS)

            db.session.add(test_user)
            db.session.commit()

    return app
