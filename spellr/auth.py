import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import generate_password_hash

from spellr.db import get_db
from spellr.util import flash_errors
from spellr.forms import RegisterForm, LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        print("success!")
        db = get_db()
        db.execute(
            "INSERT INTO user (username,password,two_factor) VALUES (?,?,?)",
            (
                form.username.data,
                generate_password_hash(form.password.data),
                form.two_factor.data,
            ),
        )
        db.commit()
        flash("Thank you for registering, you can now log in.", "success")
        return redirect(url_for("auth.login"))
    else:
        print(f"oh no! {[error for error in form.errors]}")
        flash_errors(form)
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        session.clear()
        session["user_id"] = form.user["id"]
        flash("You are logged in.", "success")
        return redirect(url_for("index"))
    else:
        flash_errors(form)
    return render_template("auth/login.html", form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
