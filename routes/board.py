from flask import (
    Blueprint,
    session,
    request,
    redirect,
    url_for,
    render_template,
)
from models.board import Board
from routes.topic import bp_topic

bp_board = Blueprint('bp_board', __name__)


@bp_board.route('/admin')
def index():
    return render_template('board/admin_index.html')


@bp_board.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Board.new(form)
    return redirect(url_for('bp_topic.index'))
