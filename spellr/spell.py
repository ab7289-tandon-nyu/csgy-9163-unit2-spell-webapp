from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

import subprocess

from spellr.auth import login_required
from spellr.db import get_db

bp = Blueprint("spell", __name__)


@bp.route("/spell_check", methods=("GET", "POST"))
def index():
    result = ""
    text = ""
    if request.method == "POST":
        text = request.form["inputtext"]
        # do stuff with output
        # result = subprocess.call...
        result = text

    return render_template("spell/index.html", orig_text=text, result=result)
