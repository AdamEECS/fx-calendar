from . import *
from flask import current_app
from models.event import Event
from models.detail import Detail
from models.news import News
from models.rate import Rate
import datetime

main = Blueprint('jsonp', __name__)


def support_jsonp(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args, **kwargs)) + ')'
            return current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)
    return decorated_function


@main.route('/events')
@support_jsonp
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


@main.route('/events/search', methods=['GET'])
@support_jsonp
def events_search():
    form = request.args
    form_search = form.to_dict()
    form_search.pop('_')
    form_search.pop('callback')
    items = Event.search_and(form_search)
    items = [i.json() for i in items]
    return json.dumps(items, indent=4)


@main.route('/event/detail', methods=['GET'])
@support_jsonp
def events_detail():
    ticker = request.args.get('ticker')
    response = None
    if ticker is not None:
        detail = Detail.find_one(ticker=ticker)
        if detail is not None:
            response = detail.json()
    return json.dumps(response, indent=4)


@main.route('/news', methods=['GET'])
@support_jsonp
def news():
    items = News.recent()
    items = [i.json() for i in items]
    return json.dumps(items, indent=4)


@main.route('/news/top', methods=['GET'])
@support_jsonp
def news_top():
    item = News.top()
    item = item.json()
    return json.dumps(item, indent=4)


@main.route('/news/after/<int:last_time_int>', methods=['GET'])
@support_jsonp
def news_after(last_time_int):
    items = News.after(last_time_int)
    items = [i.json() for i in items]
    return json.dumps(items, indent=4)


@main.route('/rates', methods=['GET'])
@support_jsonp
def rates():
    items = Rate.all()
    items = [i.json() for i in items]
    return json.dumps(items, indent=4)
