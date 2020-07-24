from flask import (
    Blueprint,
    render_template,
    request,
    abort,
)
from flask_login import login_required

from app.forms import HistoryForm, AuthHistoryForm
from app.models import User, Question
from app.util import flash_errors
from app.permissions import admin_perm, SeeHistoryPermission

bp = Blueprint("history", __name__)


@bp.route("/history", methods=("GET", "POST"))
@login_required
def history():
    """ route for authenticated users to review their question history """
    q_list = []
    user_exists = False
    user_id = None

    form = HistoryForm(request.form)
    if form.validate_on_submit():
        user_id = form.userquery.data

        user_obj = User.query.filter_by(username=user_id).first()
        user_exists = user_obj is not None
        if user_exists:
            history_perm = SeeHistoryPermission(user_obj.id)
            if not history_perm.can():
                abort(403)
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
    if item:
        see_history = SeeHistoryPermission(item.user_id)
        if not see_history.can():
            abort(403)

    return render_template("history/item.html", item_id=item_id, item=item)


@bp.route("/login_history", methods=("GET", "POST",))
@login_required
@admin_perm.require(http_exception=403)
def auth_history():
    """route for admins to see the login and logout history of other users"""

    hist_list = []
    user_exists = False
    user_id = None

    form = AuthHistoryForm(request.form)
    if form.validate_on_submit():
        user_id = form.userid.data

        user_obj = User.query.filter_by(username=user_id).first()
        user_exists = user_obj is not None
        if user_exists:
            hist_list = user_obj.auth_histories
    else:
        flash_errors(form)

    return render_template(
        "history/auth_history.html",
        form=form,
        hist_list=hist_list,
        user_exists=user_exists,
        user_id=user_id,
    )
