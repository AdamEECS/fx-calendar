from . import *
from models.event import Event
from models.detail import Detail
from models.news import News
from models.rate import Rate
from models.history import History
import datetime

main = Blueprint('index', __name__)


@main.route('/')
def index():
    items = Event.today()
    for i in items:
        i.detail = Detail.find_one(ticker=i.ticker)
        history = History.recent_by_ticker(ticker=i.ticker)
        i.history = [h.json() for h in history]
    return render_template('event.html', items=items)


@main.route('/', methods=['POST'])
def events_search():
    form = request.form
    items = Event.search_and(form)
    for i in items:
        i.detail = Detail.find_one(ticker=i.ticker)
        history = History.recent_by_ticker(ticker=i.ticker)
        i.history = [h.json() for h in history]
    return render_template('event.html', items=items)


@main.route('/holiday', methods=['GET'])
def holiday():
    return render_template('holiday.html')


@main.route('/news', methods=['GET'])
def news():
    items = News.recent()
    last_time_int = items[0].time_int
    # print(items[0])
    return render_template('news.html', items=items, last_time_int=last_time_int)


@main.route('/news/after/<int:last_time_int>', methods=['GET'])
def news_after(last_time_int):
    items = News.after(last_time_int)
    items = [i.json() for i in items]
    return json.dumps(items)


@main.route('/rates', methods=['GET'])
def rates():
    rs = Rate.all()
    return render_template('rates.html', items=rs)


@main.route('/news/structure', methods=['GET'])
def structured_news():
    keys = [
        {
            'title': '国家地区',
            'items': ['中国', '美国', '日本', '俄罗斯', '韩国', '英国', '欧盟', '德国', '法国', '瑞士', '意大利'],
        },
        {
            'title': '交易品种',
            'items': ['黄金', '原油', '天然气', '美元', '欧元', '英镑', '日元'],
        },
        {
            'title': '消息机构',
            'items': ['央行', '美联储', '外交部', '交易所', '国防部', '证监会', '发改委', 'MSCI', '路透'],
        },
        {
            'title': '新闻人物',
            'items': ['李克强', '特雷莎·梅', '特朗普', '耶伦', '默克尔', '哈蒙德', '伊丽莎白二世', '安倍晋三'],
        },
        {
            'title': '热门事件',
            'items': ['上涨', '下跌', '开盘', '收盘', '地震', '脱欧', '制裁', '发布报告', '谈判'],
        },
    ]
    keyword = request.args.get('q')
    if keyword is not None:
        items = News.content(keyword)
    else:
        items = News.recent()
    return render_template('structured_news.html', items=items, keys=keys)

# @main.route('/news/structure', methods=['GET'])
# def structured_news_search():
#     keyword = request.args.get('keyword')
#     form = dict(title_content=keyword)
#     print(form)
#     items = Event.search_and(form)
#     print(items)
#     last_time_int = items[0].time_int
#     return render_template('structured_news.html', items=items, last_time_int=last_time_int)
