import time
import json
import requests
from models.rate import Rate
from usr_util.utils import timestamp, time_str

__author__ = '3000'

headers = {
    'access-control-request-headers': 'x-ivanka-platform',
    'origin': 'https://wallstreetcn.com',
    'Upgrade - Insecure - Requests': '1',
    'Referer': 'https://wallstreetcn.com/calendar/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


def update_rates():
    url = 'https://api-prod.wallstreetcn.com/apiv1/finfo/cbrates'
    r = requests.get(url, headers=headers)
    r = r.content.decode(encoding='utf-8')
    r = json.loads(r)
    # print(r)
    data = r.get('data')
    items = data.get('items')
    for i in items:
        # print(i)
        Rate.insert_db(i)


def timer(delta, procedure):
    while True:
        # print(int(time.time()))
        try:
            procedure()
        except BaseException as e:
            print(time_str(timestamp()), 'error', e)
        time.sleep(delta)


def main():
    print('start')
    timer(24 * 3600, update_rates)


if __name__ == '__main__':
    main()
