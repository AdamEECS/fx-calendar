from . import MongoModel
from flask import current_app as app


class Detail(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('data_influence', str, ''),
            ('data_paraphrase', str, ''),
            ('focus_reason', str, ''),
            ('next_fab_time', int, -1),
            ('public_organization', str, ''),
            ('release_frequency', str, ''),
            ('remark', str, ''),
            ('statistical_method', str, ''),
            ('ticker', str, ''),
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
    def insert_db(cls, form):
        ticker = form.get('ticker', '')
        m = cls.find_one(ticker=ticker)
        if m is None:
            cls.new(form)
        else:
            m.update(form)
        return m
