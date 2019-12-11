from models import Model
from models.user import User
from models.mongobject import MongObject
import time


class Reply(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.topic_id = int(form.get('topic_id', -1))
        self.user_id = form.get('user_id', None)
        self.ct = int(time.time())
        self.ut = self.ct

    def get_user(self):
        return User.find(self.user_id)


class Reply(MongObject):
    __fields__ = MongObject.__fields__ + [
        ('content', str, ''),
        ('topic_id', int, -1),
        ('receiver_id', int, -1),
        ('user_id', int, None)
    ]

    def get_user(self):
        return User.find(self.user_id)

    def set_user_id(self, user_id):
        self.user_id = user_id
        self.save()