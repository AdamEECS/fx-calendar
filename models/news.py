from . import MongoModel
from . import timestamp
from . import time_str
from flask import current_app as app


class News(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('content', str, ''),
            ('created_at', str, ''),
            ('pic', str, ''),
            ('revise', str, ''),
            ('reviseId', str, ''),
            ('time_humans', str, ''),
            ('time_show', str, ''),
            ('time_int', int, 0),
            ('title', str, ''),
            ('title_content', str, ''),
            ('type', str, ''),
            ('url', str, ''),
            ('news_id', str, ''),
        ]
        fields.extend(super()._fields())
        return fields

    @staticmethod
    def data_fix_require(form):
        c = form.get('content')
        judge = c[0]
        if judge == '1':
            return True
        else:
            return False

    @staticmethod
    def data_fix(form):
        try:
            c = form.get('content')
            c = c.split('#')
            c_str = '{} <br> 前值: {} 预期: {} 公布: {}'.format(c[2], c[3], c[4], c[5])
        except:
            c_str = ''
        return c_str

    @classmethod
    def new(cls, form):
        news_id = form.pop('id', -1)
        print(time_str(timestamp()))
        print('*** new:', form)
        m = super().new(form)
        m.news_id = news_id
        m.save()
        return m

    @classmethod
    def insert_db(cls, form):
        id = form.get('id')
        m = cls.find_one(news_id=id)
        if m is None:
            if cls.data_fix_require(form):
                form['title_content'] = cls.data_fix(form)
            cls.new(form)
        else:
            pass
        return m

    @classmethod
    def recent(cls, limit=50):
        data = cls.find(__sort=[('time_int', -1)])
        data = data[:limit]
        return data

    @classmethod
    def after(cls, last_time_int, limit=50):
        param = dict(
            __sort=[('time_int', 1)],
            time_int={'$gt': last_time_int},
        )
        data = cls.find(**param)
        data = data[:limit]
        return data
