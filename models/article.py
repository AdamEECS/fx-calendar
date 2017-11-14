from . import MongoModel


class Article(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('url', str, ''),
            ('url_full', str, ''),
            ('article_id', str, ''),
            ('category', str, ''),
            ('title', str, ''),
            ('img', str, ''),
            ('preview', str, ''),
            ('detailed', bool, False),
        ]
        fields.extend(super()._fields())
        return fields


class ArticleDetail(MongoModel):
    @classmethod
    def _fields(cls):
        fields = [
            ('article_id', str, ''),
            ('title', str, ''),
            ('datetime', str, ''),
            ('author', str, 'Investing.com'),
            ('content', str, ''),
        ]
        fields.extend(super()._fields())
        return fields
