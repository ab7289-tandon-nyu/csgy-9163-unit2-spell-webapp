from flask import Blueprint, redirect, render_template, request, url_for

import subprocess

from flask_login import login_required
from spellr.forms import SpellForm

bp = Blueprint("spell", __name__)


@bp.route("/spell_check", methods=("GET", "POST"))
@login_required
def spell():
    form = SpellForm(request.form)
    result = ""
    text = ""
    if form.validate_on_submit():
        text = form.inputtext.data
        # do stuff with output
        with open(r"./spellr/input.txt", "r+") as f:
            f.truncate(0)
            f.write(text)

        result = subprocess.check_output(
            [
                r"./spellr/lib/spell_check/bin/spell_check",
                r"./spellr/input.txt",
                r"./spellr/lib/spell_check/res/wordlist.txt",
            ]
        )
        result = result.decode("utf-8").strip()

    return render_template("spell/index.html", form=form, orig_text=text, result=result)


@bp.route("/")
def index():
    return redirect(url_for("spell.spell"))
