import time
import json
import requests
from uuid import uuid4
from models.test import Test
from models.news import News

from urllib.parse import urlencode

__author__ = '3000'

headers = {
    'access-control-request-headers': 'x-ivanka-platform',
    'origin': 'https://wallstreetcn.com',
    'Upgrade - Insecure - Requests': '1',
    'Referer': 'https://wallstreetcn.com/calendar/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def news_clear(news):
    black_list = [
        '<a',
        '<script',
        '金十',
    ]
    content = news.get('title_content')
    if content is None:
        return False
    for i in black_list:
        if content.find(i) > -1:
            return False
    return True


def get_news():
    url_base = 'https://view.jin10.com/flash?'
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    param = dict(
        jsonpCallback='jQuery1111019658170263181396_1497502825614',
        max_time=now,
        _=1497502825618,
    )
    url = url_base + urlencode(param)
    r = requests.get(url, headers=headers)
    r = r.content.decode(encoding='utf-8')
    r = r.split('(', 1)[1][:-2]
    r = json.loads(r)
    data = r.get('data')
    # print(data)
    for i in data:
        if news_clear(i):
            i['time_int'] = int(time.mktime(time.strptime(i.get('time_show'), '%Y-%m-%d %H:%M:%S')))
            News.insert_db(i)


def fuck_get():
    get_news()


def fuck():
    print('fuck')
    param = dict(
        content=str(uuid4()),
        long=12345678901234567890,
    )
    n = Test().new(param)
    print(n)


def timer(delta, procedure):
    while True:
        # print(int(time.time()))
        procedure()
        time.sleep(delta)


def print_data():
    d = News.after(1497571351)
    print(d)


def insert_data():
    form = dict(
        content='test',
    )
    d = News.new(form)
    print(d)


def main():
    print('start')
    timer(1, fuck_get)
    # print_data()
    # insert_data()


if __name__ == '__main__':
    main()
