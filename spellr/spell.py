from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from spellr.auth import login_required
from spellr.db import get_db

bp = Blueprint("spell", __name__)


@bp.route("/")
def index():
    #  db = get_db()
    return render_template("spell/index.html")
