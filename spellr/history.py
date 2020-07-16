from flask import (
    Blueprint,
    render_template,
    request,
)
from flask_login import login_required

from spellr.forms import HistoryForm
from spellr.models import User, Question
from spellr.util import flash_errors

bp = Blueprint("history", __name__)


@bp.route("/history", methods=("GET", "POST"))
@login_required
def history():
    """ route for authenticated users to review their question history """
    q_list = []
    user_exists = True
    user_id = None

    form = HistoryForm(request.form)
    if form.validate_on_submit():
        user_id = form.userquery.data

        user_obj = User.query.filter_by(username=user_id).first()
        user_exists = user_obj is not None
        if user_exists:
            q_list = user_obj.questions
    else:
        flash_errors(form)

    return render_template(
        "history/history.html",
        form=form,
        q_list=q_list,
        user_exists=user_exists,
        user_id=user_id,
    )


@bp.route("/history/query<int:item_id>", methods=("GET",))
@login_required
def item(item_id):

    item = Question.query.get(item_id)

    return render_template("history/item.html", item_id=item_id, item=item)
