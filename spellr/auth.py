from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from flask_login import login_required, login_user, logout_user

from spellr.extensions import db, login_manager
from spellr.models import User
from spellr.util import flash_errors
from spellr.forms import RegisterForm, LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=("GET", "POST"))
def register():
    form = RegisterForm(request.form)
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
    form = LoginForm(request.form)
    if form.validate_on_submit():
        session.permanent = True
        login_user(form.user)
        flash("You are logged in.", "success")
        return redirect(url_for("index"))
    else:
        flash_errors(form)
    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
