from models import Model
from models.mongobject import MongObject
import time


class Topic(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', None)
        self.board_id = int(form.get('board_id', -1))
        self.ct = int(time.time())
        self.ut = self.ct
        self.views = form.get('views', 0)

    @classmethod
    def get_views(cls, id):
        m = cls.find(id)
        m.views += 1
        m.save()
        return m

    def get_user(self):
        from models.user import User
        m = User.find(self.user_id)
        return m

    def get_board(self):
        from models.board import Board
        m = Board.find(self.board_id)
        return m

    def replies(self):
        from models.reply import Reply
        all_reply = Reply.find_all(topic_id=self.id)
        return all_reply


class Topic(MongObject):
    __fields__ = MongObject.__fields__ + [
        ('title', str, ''),
        ('content', str, ''),
        ('user_id', int, -1),
        ('board_id', int, -1),
        ('views', int, 0)
    ]

    @classmethod
    def get_views(cls, id):
        m = cls.find(id)
        m.views += 1
        m.save()
        return m

    def get_user(self):
        from models.user import User
        m = User.find(self.user_id)
        return m

    def get_board(self):
        from models.board import Board
        m = Board.find(self.board_id)
        return m

    def replies(self):
        from models.reply import Reply
        all_reply = Reply.find_all(topic_id=self.id)
        return all_reply