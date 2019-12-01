from flask import (
    Flask,
    Blueprint,
    session,
    request,
    redirect,
    url_for,
    render_template,
)
from models.topic import Topic
from routes import current_user


bp_topic = Blueprint('bp_topic', __name__)


@bp_topic.route('/')
def index():
    topics = Topic.all()
    return render_template('topic/index.html', ms=topics)


@bp_topic.route('/new')
def new():
    return render_template('topic/new.html')


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
