import time
import json
import requests
import os
from pyquery import PyQuery as pq
from models.article import Article, ArticleDetail
from usr_util.utils import timestamp, time_str
import pyglet
import websocket

try:
    import thread
except ImportError:
    import _thread as thread


def on_message(ws, message):
    print('onmess', message)


def on_error(ws, error):
    print('onerr', error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        for i in range(5):
            time.sleep(1)
            ws.send("Hello %d" % i)
        time.sleep(1)
        # ws.close()
        print("thread terminating...")

    thread.start_new_thread(run, ())


music = pyglet.media.load('6175.mp3')

__author__ = '3000'

headers = {
    'Host': 'trade.mql5.com',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'https://trade.mql5.com/trade?callback&switch_platform=1&border=0&startup_version=5&demo_all_servers=1&user_token=0&startup_mode=create_demo',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
    'Cookie': 'lang=en; uniq=6FD6EE4E-51A3-F-171211; _fz_ssn=1514156577176061093',
}


def log(*args):
    with open("log_arts.txt", 'a+', encoding='utf8') as f:
        print(time_str(timestamp()), *args, file=f)


def cache_html(url):
    # filename = url.split('/')[-1]
    # cache = 'cache/{}.html'.format(filename)
    # if os.path.exists(cache):
    #     with open(cache, 'r', encoding='utf-8') as f:
    #         r = f.read()
    #     return pq(r)
    # else:
    #     r = requests.get(url, headers=headers)
    #     r = r.content.decode(encoding='utf-8')
    #     with open(cache, 'wt', encoding='utf-8') as f:
    #         f.write(r)
    #     return pq(r)

    # disable cache
    r = requests.get(url, headers=headers)
    r = r.content.decode(encoding='utf-8')
    return pq(r)


def connect():
    url = 'https://trade.mql5.com/trade/json'
    data = {
        'gwt': '2',
        'login': '26623520',
        'trade_server': 'MetaQuotes - Demo',
    }
    r = requests.get(url, params=data, headers=headers)
    r = r.content.decode(encoding='utf-8-sig')
    r = json.loads(r)
    print(r)
    # rows = r['rows']
    # print(rows)
    # for product in rows:
    #     if int(product['id']) > 255:
    #         for k, v in product.items():
    #             s = '{:<20}: {}'.format(k, v)
    #             print(s)
    #         music.play()
    #         pyglet.app.run()


def ws_connect():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://gwt2.mql5.com/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


def timer(delta, procedure):
    while True:
        # print(int(time.time()))
        try:
            procedure()
        except BaseException as e:
            log('error', e)
        time.sleep(delta)


def task():
    ws_connect()


def main():
    print('start')
    # timer(1, task)
    task()
    # music.play()


if __name__ == '__main__':
    main()
