import time
import json
import requests
from models.event import Event
from models.detail import Detail
from models.history import History
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


def update_detail():
    url_base = 'https://api-prod.wallstreetcn.com/apiv1/finfo/ticker/'
    detail = 'detail?ticker='
    history = 'calendar/history?ticker='
    events = Event.today()
    for i in events:
        if 'Index' in i.ticker:
            query = i.ticker
            query = query.replace(' ', '+')
            url_detail = url_base + detail + query
            url_history = url_base + history + query
            data_detail = data_from_url(url_detail)
            insert_detail(data_detail)
            data_history = data_from_url(url_history)
            insert_history(data_history, i.ticker)


def init_detail():
    url_base = 'https://api-prod.wallstreetcn.com/apiv1/finfo/ticker/'
    detail = 'detail?ticker='
    history = 'calendar/history?ticker='
    events = Event.all()
    for i in events:
        if 'Index' in i.ticker:
            query = i.ticker
            query = query.replace(' ', '+')
            url_detail = url_base + detail + query
            url_history = url_base + history + query
            data_detail = data_from_url(url_detail)
            insert_detail(data_detail)
            data_history = data_from_url(url_history)
            insert_history(data_history, i.ticker)


def data_from_url(url):
    r = requests.get(url, headers=headers)
    r = r.content.decode(encoding='utf-8')
    r = json.loads(r)
    data = r.get('data')
    return data


def insert_detail(data):
    if data:
        Detail.insert_db(data)


def insert_history(data, ticker):
    if isinstance(data, dict):
        items = data.get('items', [])
        for i in items:
            i['ticker'] = ticker
            # print(i)
            History.insert_db(i)


def timer(delta, procedure):
    while True:
        # print(int(time.time()))
        try:
            procedure()
        except BaseException as e:
            print(time_str(timestamp()), 'error', e)
        time.sleep(delta)


def show_history():
    items = History.recent_by_ticker('NAPMEMPL Index')
    print(items)
    items = [i.json() for i in items]
    print(items)


def main():
    print('start')
    # timer(10, update_event)
    # init_event()
    init_detail()
    # show_history()


if __name__ == '__main__':
    main()
