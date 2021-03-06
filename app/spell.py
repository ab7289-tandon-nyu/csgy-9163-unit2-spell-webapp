from flask import Blueprint, redirect, render_template, request, url_for, flash

import subprocess

from flask_login import login_required, current_user
from app.extensions import db
from app.forms import SpellForm
from app.models import Question
from app.util import flash_errors

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
        with open(r"./app/input.txt", "r+") as f:
            f.truncate(0)
            f.write(text)

        # subprocess allows us to run the binary spell_check file from our submodule
        result = subprocess.check_output(
            [
                # location of the spell_check binary
                r"./app/lib/a.out",
                # r"./app/lib/spell_check",
                # location of the input.txt file that we just wrote the input to
                r"./app/input.txt",
                # location of the dictionary file to check the text against
                r"./app/lib/wordlist.txt",
            ]
        )
        # decode the returned text so that we can read it nicely
        result = result.decode("utf-8").strip()

        # clear after use so as to not leave clues around about what people are
        # searching for
        with open(r"./app/input.txt", "r+") as f:
            f.truncate(0)

        # persist the user's question
        q = Question(text=text, result=result, user_id=current_user.id)
        db.session.add(q)
        db.session.commit()
        flash("success", "success")
    else:
        flash_errors(form, category="result")

    return render_template("spell/index.html", form=form, orig_text=text, result=result)


@bp.route("/")
def index():
    """ basic route - reroutes to the /spell_check endpoint """
    return redirect(url_for("spell.spell"))
