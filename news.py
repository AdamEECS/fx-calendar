import time
import json
import requests
from uuid import uuid4
from models.test import Test
from models.news import News
from usr_util.utils import timestamp
from usr_util.utils import time_str

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


def log(*args):
    with open("log_news.txt", 'a+', encoding='utf8') as f:
        print(time_str(timestamp()), *args, file=f)


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


def get_news(max_time):
    url_base = 'https://view.jin10.com/flash?'
    param = dict(
        jsonpCallback='jQuery1111019658170263181396_1497502825614',
        max_time=max_time,
        _=1497502825618,
    )
    url = url_base + urlencode(param)

    r = requests.get(url, headers=headers)
    r = r.content.decode(encoding='utf-8')
    log(r)
    try:
        r = r.split('(', 1)[1][:-2]
        r = json.loads(r)
        data = r.get('data')
        # print(data)
        for i in data:
            if news_clear(i):
                i['time_int'] = int(time.mktime(time.strptime(i.get('time_show'), '%Y-%m-%d %H:%M:%S')))
                News.insert_db(i)
    except BaseException as e:
        print('e', e)
        log('[get_news e]', e)
        # print('r', r)


def fuck_get():
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    get_news(now)


def fuck_get_p():
    t_stamp = int(time.time())
    # print(t_stamp)
    while t_stamp > 1496246400:
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t_stamp))
        # print(now)
        get_news(now)
        t_stamp -= 3600


def timer(delta, procedure):
    while True:
        # print(int(time.time()))
        try:
            log('**************** procedure *****************')
            procedure()
        except requests.exceptions.ConnectionError as e:
            print(time_str(timestamp()), 'error', e)
            log('[timer e]', e)
        time.sleep(delta)


def main():
    print('start')
    timer(3, fuck_get)
    # fuck_get_p()


if __name__ == '__main__':
    main()
