from models import Model
from models.mongobject import MongObject
import time


class Board(Model):
    def __init__(self, form):
        self.id = None
        self.title = form.get('title', '')
        self.ct = int(time.time())
        self.ut = self.ct


class Board(MongObject):
    __fields__ = MongObject.__fields__ + [
        ('title', str, '')
    ]
