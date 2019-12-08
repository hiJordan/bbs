from flask import (
    Flask,
    Blueprint,
    session,
    request,
    redirect,
    url_for,
    render_template,
)
from werkzeug.utils import secure_filename
from models.user import User
from routes.topic import bp_topic
from routes import current_user

bp_user = Blueprint('bp_user', __name__)


@bp_user.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        form = request.form
        m = User.register(form)
        if m is not None:
            return redirect(url_for('.login'))
    return render_template('user/register.html')


@bp_user.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        form = request.form
        m = User.login(form)

        if m is not None:
            session['user_id'] = m.id
            return redirect(url_for('bp_topic.index'))
    return render_template('user/login.html')


def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_file_type
    return suffix in accept_user_file_type


@bp_user.route('/add_user_img', methods=['POST'])
def add_user_img():
    import os
    from config import user_img_file_dir
    user = current_user()

    if user is None:
        return redirect(url_for('.login'))

    if 'file' not in request.files:
        return redirect(request.headers.get('Referer', 'url_for(".login")'))

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if allow_file(file.filename) is True:
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_img_file_dir, filename))
        user.user_img = filename
        user.save()

    return redirect(url_for('bp_topic.index'))


@bp_user.route('/profile/<int:id>')
def profile(id):
    user = User.find(id)
    return render_template('user/profile.html', user=user)


