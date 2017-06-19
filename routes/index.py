from . import *
from models.event import Event
from models.detail import Detail
from models.news import News
import datetime

main = Blueprint('index', __name__)


@main.route('/')
def index():
    start = datetime.date.today().strftime("%Y-%m-%d")
    end_dt = datetime.date.today() + datetime.timedelta(days=1)
    end = end_dt.strftime("%Y-%m-%d")
    form = dict(
        start=start,
        end=end,
    )
    items = Event.search_and(form)
    for i in items:
        i.detail = Detail.find_one(ticker=i.ticker)
    return render_template('event.html', items=items)


@main.route('/', methods=['POST'])
def events_search():
    form = request.form
    items = Event.search_and(form)
    for i in items:
        i.detail = Detail.find_one(ticker=i.ticker)
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

