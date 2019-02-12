import requests
from datetime import datetime

import lxml.html
import flask
from werkzeug.contrib.atom import AtomFeed

class Table(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

def extract_items(src, rootxp, titlexp, urlxp, datexp, datefmt, **kwargs):
    html = requests.get(src).content
    tree = lxml.html.fromstring(html) \
                    .xpath(rootxp)

    items = []
    for element in tree:
        item = Table()
        item.title   = element.xpath(titlexp)[0].text
        item.url     = element.xpath(urlxp)[0]
        item.updated = datetime.strptime(
            element.xpath(datexp)[0].text,
            datefmt
        )
        items.append(item)
    items.sort(
        key     = lambda i: i.updated,
        reverse = True,
    )
    return items

app = flask.Flask(__name__)

@app.route('/')
def feed():
    config = Table(
        title   = "Deluge",
        src     = "https://archiveofourown.org/works/3584145/navigate",
        rootxp  = "//ol[@class = 'chapter index group']/li",
        titlexp = "a",
        urlxp   = "a/@href",
        datexp  = "span",
        datefmt = "(%Y-%m-%d)",
    )

    items = extract_items(**config)

    feed = AtomFeed(
        title = config.title,
        url   = config.src,
        id    = config.src,
    )
    for i in items: feed.add(**i)
    return feed.get_response()
