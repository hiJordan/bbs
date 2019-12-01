from models import Model
import time


class Reply(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        self.topic_id = int(form.get('topic_id', -1))
        self.user_id = form.get('user_id', None)
        self.ct = int(time.time())
        self.ut = self.ct
