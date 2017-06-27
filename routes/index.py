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
