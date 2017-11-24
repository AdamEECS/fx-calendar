import time
import json
import requests
import os
from pyquery import PyQuery as pq
from models.article import Article, ArticleDetail
from usr_util.utils import timestamp, time_str

__author__ = '3000'

headers = {
    'access-control-request-headers': 'x-ivanka-platform',
    'Host': 'cn.investing.com',
    'Upgrade - Insecure - Requests': '1',
    'Referer': 'https://cn.investing.com/news/most-popular-news',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
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


def article(s):
    url_base = 'https://cn.investing.com'
    div = s('div.textDiv')
    a = div('a')
    title = a.text()
    url = a.attr('href')
    url_full = url_base + url
    a_id = url.split('/')[-1]
    category = url.split('/')[-2]
    img = s('a')('img').attr('src')
    preview = div('p').text()
    preview = preview.replace('Investing.com', '')
    # return title, url, img, preview
    d = {
        'url': url,
        'url_full': url_full,
        'article_id': a_id,
        'category': category,
        'title': title,
        'img': img,
        'preview': preview,
    }
    if Article.find_one(url=url):
        return Article.find_one(url=url)
    else:
        return Article.new(d)


def get_article_list(url, selector):
    # url = 'https://cn.investing.com/news/forex-news'
    doc = cache_html(url)
    div = doc(selector)
    article_raw_list = div('article.articleItem')
    article_list = [article(pq(a)) for a in article_raw_list]
    # print(article_list)


def article_detail(div, a_id):
    title = div('h1').text()
    datetime = div('div.contentSectionDetails')('span').eq(-1).text()
    author = div('div.contentSectionDetails')('a').eq(0).text()
    i = div('div.contentSectionDetails')('i')
    if i.length > 0:
        src = i('img').attr('src')
        author = src.split('/')[-1].split('.')[0]
    if '(' in datetime and ')' in datetime:
        datetime = datetime.split('(')[1].split(')')[0]
    content = div('div.WYSIWYG').html()
    d = {
        'article_id': a_id,
        'title': title,
        'author': author,
        'datetime': datetime,
        'content': content,
    }
    if ArticleDetail.find_one(article_id=a_id):
        return ArticleDetail.find_one(article_id=a_id)
    else:
        a = Article.find_one(article_id=a_id)
        a.detailed = True
        a.save()
        return ArticleDetail.new(d)


def get_article_detail(url):
    doc = cache_html(url)
    div = doc('section#leftColumn')
    a_id = url.split('/')[-1]
    d = article_detail(div, a_id)
    # print(d)


def get_article_all():
    arts = Article.find(detailed=False)
    for a in arts:
        log(a)
        get_article_detail(a.url_full)
        time.sleep(1)


def timer(delta, procedure):
    while True:
        # print(int(time.time()))
        try:
            procedure()
        except BaseException as e:
            log('error', e)
        time.sleep(delta)


def task():
    get_article_list('https://cn.investing.com/news/forex-news', 'div.largeTitle')
    time.sleep(1)
    get_article_list('https://cn.investing.com/analysis/外汇', 'div#contentSection')
    time.sleep(1)
    get_article_all()


def main():
    print('start')
    timer(3600, task)
    # get_article_detail('https://cn.investing.com/news/forex-news/article-504292')
    # get_article_detail('https://cn.investing.com/analysis/article-200218830')
    # get_article_detail('https://cn.investing.com/analysis/article-200218926')


if __name__ == '__main__':
    main()
