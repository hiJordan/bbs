from flask import (
    Blueprint,
    session,
    request,
    redirect,
    url_for,
    render_template,
)
from models.board import Board
from routes.auth import bp_user
from routes.topic import bp_topic
from routes import current_user


bp_board = Blueprint('bp_board', __name__)


def role_check():
    user = current_user()
    if user.role == 1:
        return True
    return False


@bp_board.route('/admin')
def index():
    if role_check() is False:
        return redirect(url_for('bp_user.login'))
    bs = Board.all()
    return render_template('board/admin_index.html', bs=bs)


@bp_board.route('/add', methods=['POST'])
def add():
    if role_check() is False:
        return redirect(url_for('bp_user.login'))

    form = request.form
    m = Board.new(form)
    return redirect(url_for('bp_topic.index'))


@bp_board.route('/delete/<int:board_id>')
def delete(board_id):
    if current_user() is False:
        return redirect(url_for('bp_user.login'))
    m = Board.delete(board_id)
    if m is not None:
        return redirect(url_for('.index'))
    return redirect(url_for('bp_topic.index'))
