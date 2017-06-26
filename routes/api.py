from . import *
from models.event import Event
from models.detail import Detail
from models.news import News
from models.rate import Rate
import datetime

main = Blueprint('api', __name__)


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


@main.route('/event/detail', methods=['GET'])
def events_detail():
    ticker = request.args.get('ticker')
    response = None
    if ticker is not None:
        detail = Detail.find_one(ticker=ticker)
        if detail is not None:
            response = detail.json()
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
