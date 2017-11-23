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

    @classmethod
    def find(cls, **kwargs):
        ms = super().find(**kwargs)
        # print(ms)
        for m in ms:
            import re
            m.content = re.sub('(style=").*?(")', '', m.content)
            m.content = re.sub('(<a).*?(>)', '', m.content)
            m.content = re.sub('(</a>)', '', m.content)
            m.content = m.content.replace('（以上为分析师个人观点，不代表Investing.com观点，不作为投资建议。）', '')
            m.content = m.content.replace('investing.com', '')
        return ms
