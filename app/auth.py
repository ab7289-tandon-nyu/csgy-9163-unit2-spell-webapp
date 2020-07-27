from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    session,
    current_app,
)
from flask_login import login_required, login_user, logout_user, current_user
from flask_principal import (
    Identity,
    AnonymousIdentity,
    identity_changed,
    identity_loaded,
    RoleNeed,
    UserNeed,
)

from app.extensions import db, login_manager
from app.models import User, AuthHistory
from app.util import flash_errors
from app.forms import RegisterForm, LoginForm
from app.permissions import seeHistoryNeed
from datetime import datetime

bp = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    """ loader method required by flask-login to resolve a user """
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    """ callback method required to redirect the user to the login page
    if they are unauthorized or if their session has become invalidated.
    without this the user just gets a 401 Unauthorized error, which isn't
    very helpful """
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=("GET", "POST"))
def register():
    """ registration route, allows new users to sign up """
    form = RegisterForm(request.form)
    # .validate_on_submit() is a Flask-WTF convenience function to check that the
    # request is a POST and that the form data is valid
    if form.validate_on_submit():
        new_user = User(username=form.username.data, two_factor=form.two_factor.data,)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("success, Thank you for registering, you can now log in.", "success")
        # return redirect(url_for("auth.login"))
    else:
        flash_errors(form, category="success")
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=("GET", "POST"))
def login():
    """ login route, allows registered users to login """
    form = LoginForm(request.form)
    if form.validate_on_submit():
        # setting session.permanent = True paradoxically tells flask that the session
        # should be invalidated after the PERMANENT_SESSION_LIFETIME (2 mins in this case)
        # has expired
        session.permanent = True
        # handy-dandy convenience function from Flask-Login to log in the user and add them
        # to the session
        login_user(form.user)

        # Tell flask-principal that the identity has changed
        identity_changed.send(
            current_app._get_current_object(), identity=Identity(form.user.id)
        )

        # update user's log in time
        hist = AuthHistory(login=datetime.now())
        form.user.auth_histories.append(hist)
        db.session.add(hist)
        db.session.commit()

        flash("You are logged in.", "success")
        # return redirect(url_for("index"))
    else:
        flash_errors(form, category="result")
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    """ log the user out """
    # persist the user's logout time before loging them out
    hist = (
        AuthHistory.query.filter_by(user_id=current_user.id)
        .order_by(AuthHistory.login.desc())
        .first()
    )
    hist.logout = datetime.now()
    db.session.add(hist)
    db.session.commit()

    # handy-dandy convenience function from Flask-Login to log the user out and invalidate
    # their session
    logout_user()

    # remove session keys set by Flask-Principal
    for key in ("identity.id", "identity.auth_type"):
        session.pop(key, None)

    # tell flask-principal the user is anonymous
    identity_changed.send(
        current_app._get_current_object(), identity=AnonymousIdentity()
    )
    return redirect(url_for("auth.login"))


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    """ load user roles when they log in """
    # set the identity user object
    identity.user = current_user

    # ad the userNeed to the identity
    if hasattr(current_user, "id"):
        identity.provides.add(UserNeed(current_user.id))
        identity.provides.add(seeHistoryNeed(current_user.id))

    # Assuming the User model has a list of roles, update
    # the identity with the roles that the user provides
    if hasattr(current_user, "roles"):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))
