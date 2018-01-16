import time
import json
import requests
from models.fof import Fof
from usr_util.utils import timestamp, time_str
from config.key import fof_cookie, fof_id

__author__ = '3000'

headers = {
    'Host': 'test.fofpower.com',
    'Referer': 'http://test.fofpower.com/ProductPerspective',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': fof_cookie,
}


def log(*args):
    with open("log_fof.txt", 'a+', encoding='utf8') as f:
        print(time_str(timestamp()), *args, file=f)


def get_fof(page=1, rows=20):
    url = 'http://test.fofpower.com/product/easyfind'
    data = {
        'page': page,
        'rows': rows,
        'order': 'asc',
        'is_internal': '0',
        'userId': fof_id,
        'user_id': fof_id,
        'fundName': '',
    }
    r = requests.post(url, data=data, headers=headers)
    r = r.content.decode(encoding='utf-8-sig')
    r = json.loads(r)
    # print(r)
    # with open('temp.txt', 'w+', encoding='utf-8') as f:
    #     json.dump(r, f, indent=4, ensure_ascii=False)
    rows = r.get('rows', None)
    if rows is None:
        return
    # print(len(rows))
    for i in rows:
        index = int(i.get('index', 0))
        if not Fof.find_one(index=index):
            Fof.new(i)


def timer(delta, procedure):
    while True:
        print(int(time.time()))
        try:
            procedure()
        except BaseException as e:
            log('error', e)
        time.sleep(delta)


def task():
    start = 161
    for i in range(161 - start):
        print(start + i)
        get_fof(page=start + i, rows=1000)


def main():
    print('start')
    # timer(3600, task)
    task()


if __name__ == '__main__':
    main()
