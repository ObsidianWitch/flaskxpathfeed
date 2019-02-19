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

def extract(src):
    request = requests.get(
        url     = src,
        headers = { "user-agent": "Mozilla/5.0" },
    )
    src  = request.url # resolved url
    html = request.content
    tree = lxml.html.fromstring(html)

    bridge = next(
        bridge for _, bridge in app.config.bridges.items()
        if bridge.match(src)
    )

    title = " ".join(
        xpathout(tree, "//title/text()").split()
    )

    items = []
    for element in tree.xpath(bridge.rootxp):
        item = Table()
        item.title = xpathout(element, bridge.titlexp)
        item.url = urljoin(
            src, xpathout(element, bridge.urlxp)
        ) # absolute url
        item.updated = datetime.strptime(
            xpathout(element, bridge.datexp), bridge.datefmt,
        )
        if hasattr(bridge, "descxp"):
            item.summary = xpathout(element, bridge.descxp)
        items.append(item)
    items.sort(
        key     = lambda i: i.updated,
        reverse = True,
    )

    return title, items

flaskapp = flask.Flask(__name__)

@flaskapp.route('/feed')
def feed():
    src = flask.request.args["src"]
    title, items = extract(src)
    feed = AtomFeed(
        title = title,
        url   = src,
        id    = src,
    )
    for i in items: feed.add(**i)
    return feed.get_response()
