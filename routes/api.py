from . import *
from models.event import Event
from models.detail import Detail
from models.history import History
from models.news import News
from models.rate import Rate
from models.article import Article, ArticleDetail
import datetime
from flask_cors import CORS

main = Blueprint('api', __name__)
CORS(main)


@main.route('/events')
def events():
    start = datetime.date.today().strftime("%Y-%m-%d")
    end_dt = datetime.date.today() + datetime.timedelta(days=1)
    end = end_dt.strftime("%Y-%m-%d")
    form = dict(
        start=start,
        end=end,
    )
    items = Event.search_and(form)
    items = [i.json() for i in items]
    return json.dumps(items, indent=4)


@main.route('/events', methods=['POST'])
def events_search():
    form = request.form
    items = Event.search_and(form)
    items = [i.json() for i in items]
    return json.dumps(items, indent=4)


@main.route('/fxtime', methods=['GET'])
def fxtime():
    start = request.args.get('start')
    end = request.args.get('end')
    form = dict(
        start=start,
        end=end,
    )
    items = Event.search_and(form)
    for i in items:
        i.fx_time_start = i.timestamp - 600
        i.fx_time_end = i.timestamp + 600
        i.timestamp_str = time_str(i.timestamp)
        i.fx_time_start_str = time_str(i.fx_time_start)
        i.fx_time_end_str = time_str(i.fx_time_end)
    items = [i.json() for i in items]
    return json.dumps(items, indent=4)


@main.route('/event/detail', methods=['GET'])
def event_detail():
    ticker = request.args.get('ticker')
    response = None
    if ticker is not None:
        detail = Detail.find_one(ticker=ticker)
        if detail is not None:
            response = detail.json()
    return json.dumps(response, indent=4)


@main.route('/event/history', methods=['GET'])
def event_history():
    ticker = request.args.get('ticker')
    response = None
    if ticker is not None:
        detail = History.recent_by_ticker(ticker=ticker)
        if detail is not None:
            response = [i.json() for i in detail]
    return json.dumps(response, indent=4)


@main.route('/holiday', methods=['GET'])
def holiday():
    return render_template('holiday.html')


@main.route('/news', methods=['GET'])
def news():
    items = News.recent()
    items = [i.json() for i in items]
    return json.dumps(items, indent=4)


@main.route('/news/top', methods=['GET'])
def news_top():
    item = News.top()
    item = item.json()
    return json.dumps(item, indent=4)


@main.route('/news/after/<int:last_time_int>', methods=['GET'])
def news_after(last_time_int):
    items = News.after(last_time_int)
    items = [i.json() for i in items]
    return json.dumps(items, indent=4)


@main.route('/rates', methods=['GET'])
def rates():
    items = Rate.all()
    items = [i.json() for i in items]
    return json.dumps(items, indent=4)


@main.route('/article/list/<category>', methods=['GET'])
def article_list(category):
    items = Article.find(category=category)
    items = [i.json() for i in items]
    return json.dumps(items, indent=4)


@main.route('/article/<article_id>', methods=['GET'])
def article(article_id):
    items = ArticleDetail.find_one(article_id=article_id)
    return json.dumps(items.json(), indent=4)


@main.route('/article/list/all', methods=['GET'])
def article_list_all():
    items = Article.all()
    items = [i.json() for i in items]
    return json.dumps(items, indent=4, ensure_ascii=False)


@main.route('/article/all', methods=['GET'])
def article_all():
    items = ArticleDetail.all()
    items = [i.json() for i in items]
    return json.dumps(items, indent=4, ensure_ascii=False)


@main.route('/article/all/del', methods=['GET'])
def article_all_del():
    items = ArticleDetail.all()
    items = [i for i in items if i.title == '']
    for i in items:
        i.delete()
        a = Article.find_one(article_id=i.article_id)
        a.detailed = False
        a.save()
    return 'ok'
