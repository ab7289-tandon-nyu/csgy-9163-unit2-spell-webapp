from flask import Blueprint, redirect, render_template, request, url_for

import subprocess

from spellr.auth import login_required

bp = Blueprint("spell", __name__)


@bp.route("/spell_check", methods=("GET", "POST"))
@login_required
def spell():
    result = ""
    text = ""
    if request.method == "POST":
        text = request.form["inputtext"]
        # do stuff with output
        with open(r"./spellr/input.txt", "r+") as f:
            f.truncate(0)
            f.write(text)

        result = subprocess.check_output(
            [r".spellr/lib/spell_check/bin/spell_check", r"./spellr/input.txt", r"./spellr/lib/spell_check/res/wordlist.txt"]
        )
        result = result.decode("utf-8").strip()
        # result = text

    return render_template("spell/index.html", orig_text=text, result=result)


@bp.route("/")
def index():
    return redirect(url_for("spell.spell"))
