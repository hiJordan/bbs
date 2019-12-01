from flask import (
    Flask,
    Blueprint,
    session,
    request,
    redirect,
    url_for,
    render_template,
)
from models.reply import Reply
from routes.topic import bp_topic
from routes import current_user

bp_reply = Blueprint('bp_reply', __name__)


@bp_reply.route('/add', methods=['post'])
def add():
    user = current_user()
    form = request.form
    m = Reply.new(form, user_id=user.id)
    return redirect(url_for('bp_topic.detail', id=m.topic_id))
