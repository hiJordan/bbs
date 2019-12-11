from models import Model
from models.mongobject import MongObject
import time


class Mail(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.content = form.get('content', '')

        self.receiver = form.get('receiver', '')
        self.sender_id = -1

        self.read = False
        self.ct = int(time.time())

    def set_sender(self, sender_id):
        self.sender_id = sender_id
        self.save()

    def mark_read(self):
        self.read = True
        self.save()


class Mail(MongObject):
    __fields__ = MongObject.__fields__ + [
        ('title', str, ''),
        ('content', str, ''),
        ('read', bool, False),
        ('sender_id', int, -1),
        ('receiver', str, ''),
    ]

    def set_sender(self, sender_id):
        self.sender_id = sender_id
        self.save()

    def mark_read(self):
        self.read = True
        self.save()
