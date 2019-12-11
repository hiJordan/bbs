import json
import time
from pymongo import MongoClient

mongo_client = MongoClient()


def timestamp():
    return int(time.time())


# 设置并得到表的id值
def next_id(name):
        query = {
            'name': name,
        }
        update = {
            '$inc': {
                'seq': 1
            }
        }
        kwargs = {
            'query': query,
            'update': update,
            'upsert': True,
            'new': True,
        }
        doc = mongo_client.db['data_id']
        new_id = doc.find_and_modify(**kwargs).get('seq')
        return new_id


# Model 是一个 ORM（object relation mapper）
# 好处就是不需要关心存储数据的细节，直接使用即可
class MongObject(object):
    # 字段属性
    __fields__ = [
        '_id',
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('ct', int, 0),
        ('ut', int, 0),
    ]

    # 检测一个元素是否在数据库
    @classmethod
    def has(cls, **kwargs):
        return cls.find_one(**kwargs) is not None

    # 得到一个表中的所有数据
    def mongos(self, name):
        return mongo_client.db[name].find()

    # 创建相应的对象
    @classmethod
    def new(cls, form=None, **kwargs):
        name = cls.__name__

        # 创建空对象
        m = cls()

        # 得到字段, 暂时删除_id字段
        fields = cls.__fields__.copy()
        fields.remove('_id')

        if form is None:
            form = {}

        # 将form中值赋于new的新实例--先检查键是否存在,设置其值,反之赋予其默认值
        for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                setattr(m, k, v)

        # 处理额外的参数
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError

        # 设置其他默认数据
        m.id = next_id(name)
        ts = timestamp()
        m.ct = ts
        m.ut = ts
        # m.deleted = False
        m.type = name.lower()

        m.save()
        return m

    def save(self):
        name = self.__class__.__name__
        mongo_client.db[name].save(self.__dict__)

    def delete(self):
        name = self.__class__.__name__
        query = {
            'id': self.id,
        }
        values = {
            '$set': {
                'deleted': True,
            }
        }
        mongo_client.db[name].update_one(query, values)

    # 将mongo数据格式转换为Python类对象
    @classmethod
    def _new_with_bson(cls, bson):
        m = cls()

        fields = cls.__fields__.copy()
        fields.remove('_id')

        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                setattr(m, k, v)

        setattr(m, '_id', bson['_id'])
        m.type = cls.__name__.lower()
        return m

    # 得到对应参数的表中记录,置于一个列表中返回
    @classmethod
    def _find_raw(cls, **kwargs):
        name = cls.__name__
        ds = mongo_client.db[name].find(**kwargs)
        l = [d for d in ds]
        return l

    # 将对象source属性值, 设置为属性target的值, 保存到数据库中
    @classmethod
    def _clean_field(cls, source, target):
        ms = cls._find()
        for m in ms:
            v = getattr(m, source)
            setattr(m, target, v)
            m.save()

    # 得到表中相应条件的记录并转换为python对象列表返回
    @classmethod
    def _find(cls, **kwargs):
        name = cls.__name__
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = mongo_client.db[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        # 筛选出未被删除的数据
        l = [cls._new_with_bson(d) for d in ds if d['deleted'] is False]
        return l

    @classmethod
    def all(cls):
        return cls._find()

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def find_one(cls, **kwargs):
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)

    @classmethod
    def find(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def get(cls, id):
        return cls.find_one(id=id)

    def update(self, form, hard=False):
        for k, v in form.items():
            if hard is True or hasattr(self, k):
                setattr(self, k, v)
        self.save()

    # 查询表中条件成立的记录(转换成对象返回)。
    # 若其不存在则update字典, 形成一个新对象, 反之则直接更新表数据
    @classmethod
    def upsert(cls, query_form, update_form, hard=False):
        ms = cls.find_one(**query_form)
        if ms is None:
            query_form.update(**update_form)
            ms = cls.new(query_form)
        else:
            ms.update(update_form, hard=hard)
        return ms

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def blacklist(self):
        b = [
            '_id',
        ]
        return b

    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        return d

    # 得到有title_name_id字段的表中, 其具有的数量
    def data_count(self, cls):
        name = cls.__name__
        fk = '{}_id'.format(self.__class__.__name__.lower())
        query = {
            fk: self.id,
        }
        count = mongo_client.db[name].find(query).count()
        return count



