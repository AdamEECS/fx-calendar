from . import MongoModel
from flask import current_app as app


class Event(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('accurate_flag', str, ''),
            ('actual', str, ''),
            ('calendar_type', str, ''),
            ('category_id', str, ''),
            ('country', str, ''),
            ('currency', str, ''),
            ('description', str, ''),
            ('event_row_id', str, ''),
            ('flagURL', str, ''),
            ('forecast', str, ''),
            ('importance', str, ''),
            ('influence', str, ''),
            ('level', str, ''),
            ('mark', str, ''),
            ('previous', str, ''),
            ('push_status', str, ''),
            ('related_assets', str, ''),
            ('remark', str, ''),
            ('revised', str, ''),
            ('stars', str, ''),
            ('subscribe_status', str, ''),
            ('ticker', str, ''),
            ('timestamp', int, -1),
            ('title', str, ''),
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
    def already_have_one(cls, form):
        title = form.get('title')
        timestamp = form.get('timestamp')
        return cls.find_one(title=title, timestamp=timestamp)

    @classmethod
    def insert_db(cls, form):
        m = cls.already_have_one(form)
        # print(m)
        if m is None:
            cls.new(form)
        else:
            m.update(form)
        return m
