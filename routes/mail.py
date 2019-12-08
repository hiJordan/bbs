from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
)
from models.mail import Mail
from routes import current_user


bp_mail = Blueprint('bp_mail', __name__)


@bp_mail.route('/add', methods=['POST'])
def add():
    form = request.form
    m = Mail.new(form)
    m.set_sender(current_user().id)

    return redirect(url_for('.index'))


@bp_mail.route('/index')
def index():
    user = current_user()
    send_mails = Mail.find_all(sender_id=user.id)
    received_mails = Mail.find_all(receiver=user.name)

    return render_template('/mail/index.html', send_mails=send_mails, received_mails=received_mails)


@bp_mail.route('/detail/<int:mail_id>')
def detail(mail_id):
    user = current_user()
    m = Mail.find(mail_id)
    if user.name == m.receiver:
        m.mark_read()
    if user.id == m.sender_id or user.name == m.receiver:
        return render_template('/mail/detail.html', mail_info=m)
    return redirect(url_for('.index'))



