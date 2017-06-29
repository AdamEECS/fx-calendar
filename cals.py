import time
import json
import requests
from uuid import uuid4
from models.test import Test
from models.event import Event
from models.detail import Detail
from usr_util.utils import timestamp_today
from usr_util.utils import timestamp, time_str

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
    with open("log_cals.txt", 'a+', encoding='utf8') as f:
        print(time_str(timestamp()), *args, file=f)


def get_event(start=1496246400, delta=604800):
    url = 'https://api-prod.wallstreetcn.com/apiv1/finfo/calendars?start={}&end={}'.format(start, start + delta)
    r = requests.get(url, headers=headers)
    r = r.content.decode(encoding='utf-8')
    log(r[:120])
    r = json.loads(r)
    data = r.get('data')
    items = data.get('items')
    for i in items:
        # print(i)
        Event.insert_db(i)


def init_event():
    start = 1496246400
    delta = 604800
    end = 1501516800
    while start < end:
        get_event(start)
        start += delta


def update_event():
    start, end = timestamp_today()
    get_event(start=start)


def timer(delta, procedure):
    while True:
        # print(int(time.time()))
        try:
            log('**************** procedure *****************')
            procedure()
        except BaseException as e:
            print(time_str(timestamp()), 'error', e)
            log('[timer e]', e)
        time.sleep(delta)


def main():
    print('start')
    timer(60, update_event)
    # init_event()


if __name__ == '__main__':
    main()
