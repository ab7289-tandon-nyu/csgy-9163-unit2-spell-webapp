from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from flask_login import login_required, login_user, logout_user

from app.extensions import db, login_manager
from app.models import User
from app.util import flash_errors
from app.forms import RegisterForm, LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


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
        flash("Thank you for registering, you can now log in.", "success")
        return redirect(url_for("auth.login"))
    else:
        flash_errors(form)
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
        flash("You are logged in.", "success")
        return redirect(url_for("index"))
    else:
        flash_errors(form)
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    """ log the user out """
    # handy-dandy convenience function from Flask-Login to log the user out and invalidate
    # their session
    logout_user()
    return redirect(url_for("auth.login"))
