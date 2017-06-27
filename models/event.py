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

    def blacklist(self):
        b = [
            'flagURL',
        ]
        b.extend(super().blacklist())
        return b

    @classmethod
    def today(cls):
        import datetime
        start = datetime.date.today().strftime("%Y-%m-%d")
        end_dt = datetime.date.today() + datetime.timedelta(days=1)
        end = end_dt.strftime("%Y-%m-%d")
        form = dict(
            start=start,
            end=end,
        )
        items = cls.search_and(form)
        return items
