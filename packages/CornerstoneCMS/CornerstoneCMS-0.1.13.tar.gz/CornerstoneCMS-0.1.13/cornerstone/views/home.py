from flask import Blueprint
from jinja2 import TemplateNotFound

from cornerstone.db.models import Page, Sermon
from cornerstone.settings import get_setting
from cornerstone.theming import render

home = Blueprint('home', __name__)


@home.route('/', methods=['GET'])
def index():
    context = {
        'page': Page.query.filter_by(slug='home').first()
    }
    if get_setting('sermons-on-home-page', False):
        limit = get_setting('sermons-home-page-count', 10)
        context.update({
            'sermons': Sermon.query.order_by(Sermon.date.desc()).limit(limit).all()
        })
    try:
        return render('home.html', **context)
    except TemplateNotFound:
        return render('page.html', **context)
