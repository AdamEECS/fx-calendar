from . import MongoModel
from flask import current_app as app


class Rate(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('country', str, ''),
            ('next_meeting_at', str, ''),
            ('rate', str, ''),
            ('title', str, ''),
            ('updated_at', str, ''),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def new(cls, form):
        m = super().new(form)
        m.id = int(form.get('id', -1))
        m.save()
        return m

    @classmethod
    def find_and(cls, args):
        search = {"$and": []}
        for i in args:
            i['deleted'] = i.pop('deleted', False)
            search['$and'].append(i)
        search['__sort'] = 'timestamp'
        # print('event search', search)
        ds = cls.find(**search)
        return ds

    @classmethod
    def already_have_one(cls, form):
        title = form.get('title')
        return cls.find_one(title=title)

    @classmethod
    def insert_db(cls, form):
        m = cls.already_have_one(form)
        # print(m)
        if m is None:
            cls.new(form)
        else:
            m.update(form)
        return m

    def blacklist(self):
        b = [
            'flagURL',
        ]
        b.extend(super().blacklist())
        return b
