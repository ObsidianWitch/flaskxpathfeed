import requests
from datetime import datetime
from urllib.parse import urljoin

import lxml.html
import lxml.etree
import flask
from werkzeug.contrib.atom import AtomFeed

from app.table import Table
import app.config

def xpathout(element, xpath):
    result = element.xpath(xpath)[0]
    if isinstance(result, lxml.html.HtmlElement):
        return lxml.etree.tostring(result, encoding = "unicode")
    else:
        return result

def extract(
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
    tree = lxml.html.fromstring(html)

    title = " ".join(
        xpathout(tree, "//title/text()").split()
    )

    items = []
    for element in tree.xpath(rootxp):
        item = Table()
        item.title = xpathout(element, titlexp)
        item.url = urljoin(
            src, xpathout(element, urlxp)
        ) # absolute url
        item.updated = datetime.strptime(
            xpathout(element, datexp), datefmt,
        )
        if descxp: item.summary = xpathout(element, descxp)
        items.append(item)
    items.sort(
        key     = lambda i: i.updated,
        reverse = True,
    )
    return title, items

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
    choice.src = flask.request.args["src"]
    choice.title, choice.items = extract(**choice)

    feed = AtomFeed(
        title = choice.title,
        url   = choice.src,
        id    = choice.src,
    )
    for i in choice.items: feed.add(**i)
    return feed.get_response()
