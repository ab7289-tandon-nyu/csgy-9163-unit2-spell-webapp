from flask import Blueprint, redirect, render_template, request, url_for

import subprocess

from flask_login import login_required, current_user
from spellr.extensions import db
from spellr.forms import SpellForm
from spellr.models import Question

bp = Blueprint("spell", __name__)


@bp.route("/spell_check", methods=("GET", "POST"))
@login_required
def spell():
    """ route for authenticated users to input text for spell-checking """
    form = SpellForm(request.form)
    result = ""
    text = ""
    if form.validate_on_submit():
        text = form.inputtext.data
        # since the spell_check binary requires input text to be written to file
        # we keep a input.txt file that we can clear the contents and write the
        # new text to be checked for each submission
        with open(r"./spellr/input.txt", "r+") as f:
            f.truncate(0)
            f.write(text)

        # subprocess allows us to run the binary spell_check file from our submodule
        result = subprocess.check_output(
            [
                # location of the spell_check binary
                r"./spellr/lib/spell_check/bin/spell_check",
                # location of the input.txt file that we just wrote the input to
                r"./spellr/input.txt",
                # location of the dictionary file to check the text against
                r"./spellr/lib/spell_check/res/wordlist.txt",
            ]
        )
        # decode the returned text so that we can read it nicely
        result = result.decode("utf-8").strip()

        # persist the user's question
        q = Question(text=text, result=result, user_id=current_user.id)
        db.session.add(q)
        db.session.commit()

    return render_template("spell/index.html", form=form, orig_text=text, result=result)


@bp.route("/")
def index():
    """ basic route - reroutes to the /spell_check endpoint """
    return redirect(url_for("spell.spell"))
