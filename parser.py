import time
import json
import requests
import jieba
from uuid import uuid4
from models.test import Test
from models.news import News
from usr_util.utils import timestamp
from usr_util.utils import time_str

from urllib.parse import urlencode

__author__ = '3000'

_blacklist = [
    'br',
]


def verify_word(item):
    s = item.get('word')
    # print(s, len(s))
    if len(s) <= 1:
        return False
    if s in _blacklist:
        return False
    return True


def words_from_news():
    news_obj = News.all()
    news = [i.title_content for i in news_obj]
    total = len(news)
    d = {}
    for i in news:
        l = list(jieba.cut(i))
        for j in l:
            if j in d:
                d[j] += 1
            else:
                d[j] = 1
    result = []
    for k, v in d.items():
        item = dict(
            word=k,
            num=v,
            percentage='{:.2f}%'.format(v / total * 100)
        )
        result.append(item)
    result = sorted(result, key=lambda i: i['num'])
    result.reverse()
    result_str = ['{}: {}'.format(i['word'], i['percentage']) for i in result if verify_word(i)]
    with open("result_20170623.txt", 'w+', encoding='utf8') as f:
        json.dump(result_str, f, indent=4, ensure_ascii=False)
    print(result)


def main():
    print('start')
    words_from_news()


if __name__ == '__main__':
    main()
