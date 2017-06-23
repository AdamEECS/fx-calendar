import time
import os
from usr_util.utils import timestamp, time_str

__author__ = '3000'


def auto_restart():
    s1 = 'supervisorctl restart news'
    s2 = 'supervisorctl restart cals'
    os.system(s1)
    os.system(s2)
    with open("log_restart.txt", 'a+', encoding='utf8') as f:
        f.write('{}: restart'.format(time_str(timestamp())))


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
    timer(24 * 60, auto_restart)
    # auto_restart()


if __name__ == '__main__':
    main()
