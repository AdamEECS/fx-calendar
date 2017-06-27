from . import MongoModel
from . import timestamp
from flask import current_app as app


class History(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('ticker', str, ''),
            ('forecast', str, ''),
            ('actual', str, ''),
            ('human_date', str, ''),
            ('timestamp', int, -1),
        ]
        fields.extend(super()._fields())
        return fields

    @classmethod
    def new(cls, form):
        m = super().new(form)
        m.save()
        return m

    @classmethod
    def insert_db(cls, form):
        ticker = form.get('ticker', '')
        timestamp = form.get('timestamp', -1)
        m = cls.find_one(ticker=ticker, timestamp=timestamp)
        if m is None:
            cls.new(form)
        else:
            m.update(form)
        return m

    @classmethod
    def recent_by_ticker(cls, ticker, limit=6):
        ts = {'$lte': timestamp()}
        data = cls.find(ticker=ticker, timestamp=ts, __sort=[('timestamp', -1)])
        data = data[:limit]
        data.reverse()
        return data

    def blacklist(self):
        b = [
            'ct',
            'ut',
            'deleted',
            'uuid',
            'type',
            'id',
        ]
        b.extend(super().blacklist())
        return b
