import requests
from datetime import datetime
from urllib.parse import urljoin

import lxml.html
import lxml.etree
import flask
from werkzeug.contrib.atom import AtomFeed

from app.table import Table
import app.config

def extract_items(
    src, rootxp, titlexp, urlxp, datexp, datefmt,
    descxp = None,
    **kwargs,
):
    request = requests.get(
        url     = src,
        headers = { "user-agent": "Mozilla/5.0" },
    )
    src  = request.url # resolved url
    html = request.content
    tree = lxml.html.fromstring(html) \
                    .xpath(rootxp)

    items = []
    for element in tree:
        item = Table()
        item.title = element.xpath(titlexp)[0].text
        item.url   = urljoin(
            src, element.xpath(urlxp)[0],
        ) # absolute url
        item.updated = datetime.strptime(
            element.xpath(datexp)[0].text,
            datefmt
        )
        if descxp:
            item.summary = element.xpath(descxp)[0].text
        elif descxp is not None:
            item.summary = lxml.etree.tostring(element, encoding = "unicode")
        items.append(item)
    items.sort(
        key     = lambda i: i.updated,
        reverse = True,
    )
    return items

flaskapp = flask.Flask(__name__)

@flaskapp.route('/')
def index():
    return flask.render_template("index.html",
        bridges = app.config.bridges,
    )

@flaskapp.route('/feed')
def feed():
    choice = app.config.bridges[
        flask.request.args["bridge"]
    ]
    choice.title = flask.request.args["title"]
    choice.src = flask.request.args["src"]

    items = extract_items(**choice)

    feed = AtomFeed(
        title = choice.title,
        url   = choice.src,
        id    = choice.src,
    )
    for i in items: feed.add(**i)
    return feed.get_response()
