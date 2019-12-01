from flask import (
    Flask,
    Blueprint,
    session,
    request,
    redirect,
    url_for,
    render_template,
)
from models.user import User
from routes.topic import bp_topic
from routes import current_user

bp_user = Blueprint('bp_user', __name__)


@bp_user.route('/register', methods=['post', 'get'])
def register():
    if request.method == 'post':
        form = request.form
        m = User.register(form)
        if m is not None:
            return redirect('.login')
    return render_template('user/register.html')


@bp_user.route('/login', methods=['post', 'get'])
def login():
    if request.method == 'post':
        form = request.form
        m = User.login(form)
        if m is not None:
            session['user_id'] = m.id
            return redirect(url_for('bp_topic.index'))
    return render_template('user/login.html')


@bp_user.route('/profile')
def profile():
    user = current_user()
    return render_template('user/profile.html', user=user)


