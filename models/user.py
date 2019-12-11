from models import Model
from models.mongobject import MongObject

class User(Model):
    def __init__(self, form):
        self.id = None
        self.role = 11
        self.name = form.get('name', '')
        self.password = form.get('pass', '')
        self.user_img = 'default.png'

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib

        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    @classmethod
    def register(cls, form):
        user = cls(form)

        if len(user.name) > 2 and User.find_by(name=user.name) is None:
            m = User.new(form)
            m.password = m.salted_password(user.password)
            m.save()
            return m
        return None

    @classmethod
    def login(cls, form):
        u = User(form)
        user = User.find_by(name=u.name)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None


class User(MongObject):
    __fields__ = MongObject.__fields__ + [
        ('name', str, ''),
        ('role', int, 11),
        ('password', str, ''),
        ('user_img', str, ''),
    ]

    """
        User 是一个保存用户数据的 model
        现在只有两个属性 username 和 password
    """

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib

        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    @classmethod
    def register(cls, form):
        name = form.get('name', '')
        password = form.get('pass', '')

        if len(name) > 2 and User.find_by(name=name) is None:
            m = User.new(form)
            m.password = m.salted_password(password)
            m.save()
            return m
        return None

    @classmethod
    def login(cls, form):
        u = User()
        u.name = form.get('name', '')
        u.password = form.get('pass', '')
        user = User.find_by(name=u.name)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None
