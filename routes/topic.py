from flask import (
    Blueprint,
    session,
    request,
    redirect,
    url_for,
    render_template,
    send_from_directory,
)
from models.topic import Topic
from models.board import Board
from routes import current_user


bp_topic = Blueprint('bp_topic', __name__)


@bp_topic.route('/')
def index():
    board_id = int(request.args.get('board_id', 0))
    if board_id == 0:
        topics = Topic.all()
    else:
        topics = Topic.find_all(board_id=board_id)
    boards = Board.all()
    return render_template('topic/index.html', ms=topics, bs=boards)


@bp_topic.route('/new')
def new():
    bs = Board.all()
    return render_template('topic/new.html', bs=bs)


@bp_topic.route('/add', methods=['post'])
def add():
    user = current_user()
    form = request.form
    m = Topic.new(form, user_id=user.id)
    return redirect(url_for('.detail', id=m.id))


@bp_topic.route('/<int:id>')
def detail(id):
    user = current_user()
    m = Topic.get(id)
    return render_template('topic/detail.html', topic=m, user=user)


@bp_topic.route('/upload/<filename>')
def upload(filename):
    from config import user_img_file_dir
    return send_from_directory(user_img_file_dir, filename)
