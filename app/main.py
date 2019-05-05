import requests
from datetime import datetime
from urllib.parse import urljoin

import lxml.html
import lxml.etree
import flask
from werkzeug.contrib.atom import AtomFeed

from app.types import Table
import app.bridges

# Apply `xpath` to `element` and retrieve one result. The result is converted
# to a string if needed. Returns `default` if it is set and no result were
# retrieved.
def xpathout(element, xpath, default = None):
    result = element.xpath(xpath)
    if (not result) and (default is not None):
        result = default
    else:
        result = result[0]

    if isinstance(result, lxml.html.HtmlElement):
        return lxml.etree.tostring(result, encoding = "unicode")
    else:
        return result

# Convert all urls from the HTML `tree` to absolute ones by combining them with
# `base`.
def urlabs(tree, base):
    for element in tree.xpath('//*[@src]'):
        url = urljoin(base, element.get('src'))
        element.set('src', url)
    for element in tree.xpath('//*[@href]'):
        url = urljoin(base, element.get('href'))
        element.set('href', url)

# Extract elements needed to create a feed from the `src` web page. Elements are
# extracted using XPath expressions defined in bridges.
def extract(src):
    request = requests.get(
        url     = src,
        headers = { "user-agent": "Mozilla/5.0" },
    )
    src  = request.url # resolved url
    html = request.content
    tree = lxml.html.fromstring(html)
    urlabs(tree, src)

    bridge = next(
        bridge for _, bridge in app.bridges.table.items()
        if bridge.match(src)
    )

    title = " ".join( xpathout(tree, "//title/text()").split() )

    items = []
    for element in tree.xpath(bridge.rootxp):
        item = Table()
        item.title = xpathout(element, bridge.titlexp)
        item.url = xpathout(element, bridge.urlxp)
        item.updated = datetime.strptime(
            xpathout(element, bridge.datexp),
            bridge.datefmt,
        )
        item.id = f"{item.url}/{item.updated.isoformat()}"
        if bridge.idxp:
            item.id += f"/{xpathout(element, bridge.idxp, default = '')}"
        if bridge.descxp:
            item.summary = xpathout(element, bridge.descxp)
        items.append(item)

    if bridge.reverse: items = items[::-1]

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

@flaskapp.route('/preview')
def preview():
    src = flask.request.args["src"]
    title, items = extract(src)
    return flask.render_template("preview.html",
        title = title,
        url   = src,
        items = items,
    )
